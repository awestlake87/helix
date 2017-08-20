from contextlib import contextmanager

from .exprs import *

from ..err import ReturnTypeMismatch

def gen_code(fun, scope, ast):
    class Context:
        def __init__(self, fun, scope, ast):
            self.fun = fun
            self.scope = scope
            self.ast = ast

            self.loop_context = None

            self.entry = self.fun.get_llvm_value().append_basic_block("entry")
            self.builder = ir.IRBuilder(self.entry)

            self.body = self.builder.append_basic_block("body")
            self.builder.branch(self.body)
            self.builder.position_at_end(self.body)

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
        ctx.builder.ret(
            gen_implicit_cast_ir(
                ctx, value, ctx.fun.type.ret_type
            ).get_llvm_value()
        )

    except Exception as e:
        raise ReturnTypeMismatch()

def gen_if_statement_code(ctx, statement):
    assert statement.scope is not None

    with ctx.use_scope(statement.scope):
        assert len(statement.if_branches) >= 1

        end_if = ctx.builder.append_basic_block("end_if")
        then_block = ctx.builder.append_basic_block("then")
        else_block = ctx.builder.append_basic_block("else")

        num = len(statement.if_branches)

        all_paths_return = True

        for branch in statement.if_branches:
            condition, block = branch

            ctx.builder.cbranch(
                gen_as_bit_ir(
                    ctx, gen_expr_ir(ctx, condition)
                ).get_llvm_value(),
                then_block,
                else_block
            )

            with ctx.builder.goto_block(then_block):
                gen_block_code(ctx, block)

                if not ctx.builder.block.is_terminated:
                    ctx.builder.branch(end_if)
                    all_paths_return = False

            assert then_block.is_terminated

            ctx.builder.position_at_start(else_block)

            if branch is not statement.if_branches[-1]:
                then_block = ctx.builder.append_basic_block("then")
                else_block = ctx.builder.append_basic_block("else")


        with ctx.builder.goto_block(else_block):
            if statement.else_block is not None:
                gen_block_code(ctx, statement.else_block)

                if not ctx.builder.block.is_terminated:
                    ctx.builder.branch(end_if)
                    all_paths_return = False

            else:
                ctx.builder.branch(end_if)
                all_paths_return = False

        assert else_block.is_terminated
        assert not end_if.is_terminated

        ctx.builder.position_at_start(end_if)

        if all_paths_return:
            ctx.builder.unreachable()

def gen_loop_statement_code(ctx, statement):
    assert statement.scope is not None

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
