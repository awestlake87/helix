from contextlib import contextmanager

from ..exprs import *

from ...err import ReturnTypeMismatch

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

            self.entry = self.fun.get_llvm_value().append_basic_block("entry")
            self.builder = ir.IRBuilder(self.entry)

            self.body = self.builder.append_basic_block("body")
            self.builder.branch(self.body)
            self.builder.position_at_end(self.body)

            self._unreachable = None

            self._cleanup_blocks = [ ]

            self._return_value = StackValue(
                self, self.fun.type.ret_type
            )

            self._return_block = self.builder.append_basic_block("return")

            with self.builder.goto_block(self._return_block):
                self.builder.ret(self._return_value.get_llvm_value())

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
            self.builder.store(
                gen_implicit_cast_ir(
                    self, value, self._return_value.type
                ).get_llvm_value(),
                self._return_value.get_llvm_ptr()
            )

            self.builder.branch(
                self.control_path.gen_unwind_cleanup(self, self._return_block)
            )

    ctx = Context(fun, scope, ast)

    for arg, param_type, param_id in zip(
        ctx.fun.get_llvm_value().args,
        ctx.fun.type.param_types,
        ctx.ast.param_ids
    ):
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

def gen_return_statement_code(ctx, statement):
    value = gen_expr_ir(ctx, statement.expr)

    try:
        ctx.create_return(value)

    except Exception as e:
        raise ReturnTypeMismatch()

    ctx.control_path.is_terminated = True

def gen_if_statement_code(ctx, statement):
    assert statement.scope is not None

    if_control_path = ctx.control_path.fork()

    with ctx.use_control_path(if_control_path):
        with ctx.use_scope(statement.scope):
            assert len(statement.if_branches) >= 1

            end_if = ctx.builder.append_basic_block("end_if")
            then_block = ctx.builder.append_basic_block("then")
            else_block = ctx.builder.append_basic_block("else")

            num = len(statement.if_branches)

            for branch in statement.if_branches:
                condition, block = branch

                ctx.builder.cbranch(
                    gen_as_bit_ir(
                        ctx, gen_expr_ir(ctx, condition)
                    ).get_llvm_value(),
                    then_block,
                    else_block
                )

                ctx.builder.position_at_start(then_block)
                gen_block_code(ctx, block)

                if not ctx.builder.block.is_terminated:
                    ctx.builder.branch(end_if)

                ctx.builder.position_at_start(else_block)

                if branch is not statement.if_branches[-1]:
                    then_block = ctx.builder.append_basic_block("then")
                    else_block = ctx.builder.append_basic_block("else")

            ctx.builder.position_at_start(else_block)

            if statement.else_block is not None:
                gen_block_code(ctx, statement.else_block)

            else:
                # need empty control path so parent control path knows it
                # didn't terminate
                ctx.control_path.fork()

            if not ctx.builder.block.is_terminated:
                ctx.builder.branch(end_if)

        ctx.builder.position_at_start(end_if)

    if if_control_path.is_terminated:
        ctx.builder.branch(ctx.unreachable)

def gen_loop_statement_code(ctx, statement):
    assert statement.scope is not None

    control_path = ctx.control_path.fork()

    with ctx.use_control_path(control_path):
        with ctx.use_scope(statement.scope):
            if statement.for_clause is not None:
                gen_expr_ir(ctx, statement.for_clause)

            if statement.each_clause is not None:
                raise Todo("each clause")

            loop_head = None
            loop_body = ctx.builder.append_basic_block("loop_body")
            loop_then = ctx.builder.append_basic_block("loop_then")
            loop_exit = ctx.builder.append_basic_block("loop_exit")

            if statement.while_clause is not None:
                loop_head = ctx.builder.append_basic_block("loop_head")

                with ctx.builder.goto_block(loop_head):
                    ctx.builder.cbranch(
                        gen_as_bit_ir(
                            ctx, gen_expr_ir(ctx, statement.while_clause)
                        ).get_llvm_value(),
                        loop_body,
                        loop_exit
                    )
            else:
                loop_head = loop_body

            ctx.builder.branch(loop_head)

            ctx.builder.position_at_start(loop_body)
            with ctx.use_loop_context(loop_then, loop_exit):
                gen_block_code(ctx, statement.loop_body)

            if not ctx.builder.block.is_terminated:
                ctx.builder.branch(loop_then)


            with ctx.builder.goto_block(loop_then):
                if statement.then_clause is not None:
                    gen_expr_ir(ctx, statement.then_clause)

                if statement.until_clause is not None:
                    ctx.builder.cbranch(
                        gen_as_bit_ir(
                            ctx, gen_expr_ir(ctx, statement.until_clause)
                        ).get_llvm_value(),
                        loop_exit,
                        loop_head
                    )
                else:
                    ctx.builder.branch(loop_head)

                if not loop_then.is_terminated:
                    ctx.builder.branch(loop_exit)

            ctx.builder.position_at_start(loop_exit)

def gen_break_statement_code(ctx, _):
    if ctx.loop_context is None:
        raise Todo()

    ctx.builder.branch(ctx.loop_context.loop_exit)

def gen_continue_statement_code(ctx, _):
    if ctx.loop_context is None:
        raise Todo()

    ctx.builder.branch(ctx.loop_context.loop_then)

def gen_switch_statement_code(ctx, statement):
    assert statement.scope is not None

    control_path = ctx.control_path.fork()

    with ctx.use_control_path(control_path):
        with ctx.use_scope(statement.scope):
            value = gen_expr_ir(ctx, statement.value)
            concrete_type = get_concrete_type(value.type)

            if type(concrete_type) is IntType:
                default_block = ctx.builder.append_basic_block("default")

                inst = ctx.builder.switch(
                    gen_implicit_cast_ir(
                        ctx, value, concrete_type
                    ).get_llvm_value(),
                    default_block
                )

                for case_values, case_block in statement.case_branches:
                    block = ctx.builder.append_basic_block("case")

                    for expr in case_values:
                        value = gen_implicit_cast_ir(
                            ctx, gen_expr_ir(ctx, expr), concrete_type
                        )

                        inst.add_case(
                            value.get_llvm_value(),
                            block
                        )

                    with ctx.builder.goto_block(block):
                        gen_block_code(ctx, case_block)

                with ctx.builder.goto_block(default_block):
                    gen_block_code(ctx, statement.default_block)

            else:
                raise Todo("non-integer switches")

def gen_try_statement_code(ctx, statement):
    lpad_block = ctx.builder.append_basic_block("lpad")
    try_end = ctx.builder.append_basic_block("try_end")

    try_control_path = ctx.control_path.fork()

    with ctx.use_control_path(try_control_path):
        with ctx.use_try_context(lpad_block):
            gen_block_code(ctx, statement.try_block)

            if not ctx.builder.block.is_terminated:
                ctx.builder.branch(try_end)

        personality = None

        try:
            personality = ctx.builder.module.get_global("__gxx_personality_v0")

        except KeyError as e:
            personality = ir.Function(
                ctx.builder.module,
                ir.FunctionType(ir.IntType(32), [ ], True),
                "__gxx_personality_v0"
            )

        ctx.builder.function.attributes.personality = personality

        eh_for_intrinsic = None

        try:
            eh_for_intrinsic = ctx.builder.module.get_global(
                "llvm.eh.typeid.for"
            )
        except KeyError as e:
            eh_for_intrinsic = ir.Function(
                ctx.builder.module,
                ir.FunctionType(
                    ir.IntType(32),
                    [ ir.IntType(8).as_pointer() ]
                ),
                "llvm.eh.typeid.for"
            )

        begin_catch = None

        try:
            begin_catch = ctx.builder.module.get_global(
                "__cxa_begin_catch"
            )

        except KeyError as e:
            begin_catch = ir.Function(
                ctx.builder.module,
                ir.FunctionType(
                    ir.IntType(8).as_pointer(),
                    [ ir.IntType(8).as_pointer() ]
                ),
                "__cxa_begin_catch"
            )

        ctx.builder.position_at_start(lpad_block)
        lpad = ctx.builder.landingpad(
            ir.LiteralStructType(
                [ ir.IntType(8).as_pointer(), ir.IntType(32) ]
            )
        )
        lpad_value = ctx.builder.extract_value(lpad, 1)

        lpad_elif_block = None

        def create_cleanup_block(ctx, next_block):
            end_catch = None

            try:
                end_catch = ctx.builder.module.get_global(
                    "__cxa_end_catch"
                )

            except KeyError as e:
                end_catch = ir.Function(
                    ctx.builder.module,
                    ir.FunctionType(ir.VoidType(), [ ]),
                    "__cxa_end_catch"
                )

            block = ctx.builder.append_basic_block("catch_cleanup")

            with ctx.builder.goto_block(block):
                ctx.builder.call(end_catch, [ ])
                ctx.builder.branch(next_block)

            return block

        for clause in statement.catch_clauses:
            catch_type = gen_expr_ir(ctx, clause.type)
            type_info = None

            if type(catch_type) is PtrType:
                type_info = get_rtti_info(ctx, catch_type.pointee)

            else:
                raise Todo(catch_type)

            lpad.add_clause(ir.CatchClause(type_info))

            cmp_value = ctx.builder.call(
                eh_for_intrinsic,
                [
                    ctx.builder.bitcast(
                        type_info, ir.IntType(8).as_pointer()
                    )
                ]
            )

            catch_block = ctx.builder.append_basic_block("catch")
            lpad_elif_block = ctx.builder.append_basic_block("lpad_elif")

            ctx.builder.cbranch(
                ctx.builder.icmp_unsigned("==", lpad_value, cmp_value),
                catch_block,
                lpad_elif_block
            )

            ctx.builder.position_at_start(catch_block)

            assert clause.scope is not None

            e_value = ctx.builder.extract_value(lpad, 0)

            e_ptr = ctx.builder.call(
                begin_catch, [ e_value ]
            )

            if type(catch_type) is PtrType:
                clause.scope.resolve(clause.id).set_ir_value(
                    LlvmValue(
                        catch_type,
                        ctx.builder.bitcast(
                            e_ptr, catch_type.get_llvm_value()
                        )
                    )
                )

            catch_control_path = ctx.control_path.fork()
            catch_control_path.will_need_cleanup = True

            catch_control_path.push_cleanup(create_cleanup_block)

            with ctx.use_control_path(catch_control_path):
                with ctx.use_scope(clause.scope):
                    gen_block_code(ctx, clause.block)

            if not catch_control_path.is_terminated:
                ctx.builder.branch(try_end)


            ctx.builder.position_at_start(lpad_elif_block)

        if statement.default_catch is not None:
            lpad.add_clause(ir.CatchClause(ir.IntType(8).as_pointer()(None)))

            e_value = ctx.builder.extract_value(lpad, 0)
            e_ptr = ctx.builder.call(
                begin_catch, [ e_value ]
            )

            catch_control_path = ctx.control_path.fork()
            catch_control_path.will_need_cleanup = True

            catch_control_path.push_cleanup(create_cleanup_block)

            with ctx.use_control_path(catch_control_path):
                gen_block_code(ctx, statement.default_catch)

            if not catch_control_path.is_terminated:
                ctx.builder.branch(try_end)

        else:
            ctx.builder.resume(lpad)

        ctx.builder.position_at_start(try_end)

    if try_control_path.is_terminated:
        ctx.builder.branch(ctx.unreachable)


def gen_throw_statement_code(ctx, statement):
    throw_value = gen_expr_ir(ctx, statement.expr)
    throw_value = gen_implicit_cast_ir(
        ctx, throw_value, get_concrete_type(throw_value.type)
    )

    alloc_exception = None
    throw_exception = None

    try:
        alloc_exception = ctx.builder.module.get_global(
            "__cxa_allocate_exception"
        )

    except KeyError as e:
        alloc_exception = ir.Function(
            ctx.builder.module,
            ir.FunctionType(
                ir.IntType(8).as_pointer(),
                [ ir.IntType(64) ]
            ),
            "__cxa_allocate_exception"
        )

    try:
        throw_exception = ctx.builder.module.get_global(
            "__cxa_throw"
        )

    except KeyError as e:
        throw_exception = ir.Function(
            ctx.builder.module,
            ir.FunctionType(
                ir.VoidType(),
                [
                    ir.IntType(8).as_pointer(),
                    ir.IntType(8).as_pointer(),
                    ir.IntType(8).as_pointer()
                ]
            ),
            "__cxa_throw"
        )

    type_info = get_rtti_info(ctx, throw_value.type)
    exception_buffer = ctx.builder.call(
        alloc_exception,
        [
            gen_cast_ir(
                ctx,
                gen_sizeof_ir(ctx, throw_value), IntType(64)
            ).get_llvm_value()
        ]
    )

    ctx.builder.store(
        throw_value.get_llvm_value(),
        ctx.builder.bitcast(
            exception_buffer, PtrType(throw_value.type).get_llvm_value()
        )
    )


    assert type_info is not None
    assert exception_buffer is not None

    throw_args = [
        exception_buffer,
        ctx.builder.bitcast(type_info, ir.IntType(8).as_pointer()),
        ir.IntType(8).as_pointer()(None)
    ]

    if ctx.try_context is not None:
        ctx.builder.invoke(
            throw_exception,
            throw_args,
            ctx.unreachable,
            ctx.try_context.unwind_to
        )

    else:
        ctx.builder.call(throw_exception, throw_args)

    ctx.control_path.is_terminated = True
