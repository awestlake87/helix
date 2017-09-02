from contextlib import contextmanager

from ..exprs import *

from .if_statement import *
from .loop_statement import *
from .return_statement import *
from .switch_statement import *
from .try_statement import *

class ControlPath:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = [ ]

        self.cleanup_creators = [ ]

        self._is_terminated = False
        self.will_need_cleanup = False

    def fork(self):
        child = ControlPath(self)
        self.children.append(child)
        return child

    @property
    def is_terminated(self):
        if self._is_terminated:
            return True

        elif self.children:
            for child in self.children:
                if not child.is_terminated:
                    return False

            return True

        else:
            return False

    @is_terminated.setter
    def is_terminated(self, flag):
        self._is_terminated = flag

    @property
    def needs_cleanup(self):
        if self.is_terminated:
            return False

        elif self.cleanup_creators:
            return True

        else:
            return False

    def push_cleanup(self, create_cleanup):
        self.cleanup_creators.append(create_cleanup)

    def gen_cleanup(self, ctx, next_block):
        next_cleanup = next_block

        for creator in self.cleanup_creators:
            next_cleanup = creator(ctx, next_cleanup)

        return next_cleanup

    def gen_unwind_cleanup(self, ctx, next_block, until_control_path=None):
        if self.parent is until_control_path:
            return self.gen_cleanup(ctx, next_block)

        elif self.parent is None:
            raise Todo("unable to unwind to control path")

        else:
            return self.gen_cleanup(
                ctx,
                self.parent.gen_unwind_cleanup(
                    ctx, next_block, until_control_path
                )
            )

def gen_code(fun, scope, ast):
    class Context:
        def __init__(self, fun, scope, ast):
            self.fun = fun
            self.scope = scope
            self.ast = ast

            self.const_string_counter = 0
            self.loop_context = None
            self.try_context = None
            self.instance = None

            self.entry = self.fun.get_llvm_value().append_basic_block("entry")
            self.builder = ir.IRBuilder(self.entry)

            self.body = self.builder.append_basic_block("body")
            self.builder.branch(self.body)
            self.builder.position_at_end(self.body)

            self._unreachable = None

            self._cleanup_blocks = [ ]

            if type(self.fun.type.ret_type) is not VoidType:
                self._return_value = StackValue(
                    self, self.fun.type.ret_type
                )
            else:
                self._return_value = None

            self._return_block = self.builder.append_basic_block("return")

            with self.builder.goto_block(self._return_block):
                if self._return_value is not None:
                    self.builder.ret(self._return_value.get_llvm_value())
                else:
                    self.builder.ret_void()
                
            self.control_path = ControlPath()

        @property
        def unreachable(self):
            if self._unreachable is None:
                self._unreachable = self.builder.append_basic_block(
                    "unreachable"
                )

                with self.builder.goto_block(self._unreachable):
                    self.builder.unreachable()

            return self._unreachable

        @contextmanager
        def use_scope(self, scope):
            old_scope = self.scope
            self.scope = scope

            yield

            self.scope = old_scope

        @contextmanager
        def use_loop_context(self, loop_then, loop_exit):
            class LoopContext:
                def __init__(self, loop_then, loop_exit):
                    self.loop_then = loop_then
                    self.loop_exit = loop_exit

            old_ctx = self.loop_context
            self.loop_context = LoopContext(loop_then, loop_exit)

            yield

            self.loop_context = old_ctx


        @contextmanager
        def use_try_context(self, unwind_to):
            class TryContext:
                def __init__(self, unwind_to):
                    self.unwind_to = unwind_to

            old_ctx = self.try_context
            self.try_context = TryContext(unwind_to)

            yield

            self.try_context = old_ctx


        @contextmanager
        def push_cleanup(self, create_cleanup_block):
            self._cleanup_blocks.append(
                create_cleanup_block(
                    self._cleanup_blocks[-1]
                    if self._cleanup_blocks else
                    self._return_block
                )
            )

            yield

            self._cleanup_blocks.pop()

        @contextmanager
        def use_control_path(self, control_path):
            old_control_path = self.control_path
            self.control_path = control_path

            yield

            if self.control_path.needs_cleanup:
                continue_block = ctx.builder.append_basic_block("continue")

                cleanup = self.control_path.gen_cleanup(self, continue_block)

                ctx.builder.branch(cleanup)
                ctx.builder.position_at_start(continue_block)

            self.control_path = old_control_path


        def create_return(self, value = None):
            if self._return_value is not None:
                self.builder.store(
                    gen_implicit_cast_ir(
                        self, value, self._return_value.type
                    ).get_llvm_value(),
                    self._return_value.get_llvm_ptr()
                )
            elif value is not None:
                raise Todo("attempting to return value in void fun")

            self.builder.branch(
                self.control_path.gen_unwind_cleanup(self, self._return_block)
            )

    ctx = Context(fun, scope, ast)

    params = None

    if ast.is_attr:
        ctx.instance = LlvmRef(
            ctx,
            ctx.fun.type.param_types[0].pointee,
            ctx.fun.get_llvm_value().args[0]
        )

        params = zip(
            ctx.fun.get_llvm_value().args[1:],
            ctx.fun.type.param_types[1:],
            ctx.ast.param_ids
        )

    else:
        params = zip(
            ctx.fun.get_llvm_value().args,
            ctx.fun.type.param_types,
            ctx.ast.param_ids
        )


    for arg, param_type, param_id in params:
        value = StackValue(ctx, param_type)

        gen_assign_code(ctx, value, LlvmValue(param_type, arg))

        ctx.scope.resolve(param_id).set_ir_value(value)

    gen_block_code(ctx, ast.body)

def gen_block_code(ctx, block):
    assert block.scope is not None

    control_path = ctx.control_path.fork()

    with ctx.use_control_path(control_path):
        with ctx.use_scope(block.scope):
            for statement in block.statements:
                gen_statement_code(ctx, statement)


def gen_statement_code(ctx, statement):
    statement_type = type(statement)

    if statement_type is ReturnNode:
        gen_return_statement_code(ctx, statement)

    elif statement_type is IfStatementNode:
        gen_if_statement_code(ctx, statement)

    elif statement_type is LoopStatementNode:
        gen_loop_statement_code(ctx, statement)

    elif statement_type is SwitchStatementNode:
        gen_switch_statement_code(ctx, statement)

    elif statement_type is TryStatementNode:
        gen_try_statement_code(ctx, statement)

    elif statement_type is ThrowStatementNode:
        gen_throw_statement_code(ctx, statement)

    elif statement_type is BreakNode:
        gen_break_statement_code(ctx, statement)

    elif statement_type is ContinueNode:
        gen_continue_statement_code(ctx, statement)

    elif statement_type is FunNode or statement_type is StructNode:
        # only interested in generating the current fun
        pass

    elif issubclass(statement_type, ExprNode):
        gen_expr_ir(ctx, statement)

    else:
        raise Todo(statement)
