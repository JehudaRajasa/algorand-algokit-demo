import beaker
import pyteal as pt

class AppState:
    # set the variable name
    counter_global = beaker.GlobalStateValue(
        # set type uint
        stack_type=pt.TealType.uint64,
        # set a default of zero
        default=pt.Int(0)
    )

app = beaker.Application("simple_counter", state=AppState())

# The @app.external states that this function call be called externally
@app.external
def increment_global(*, output: pt.abi.Uint64) -> pt.Expr:
    return pt.Seq(
        # here we get the counter_global item from the state, and set it to it's current value + 1
        app.state.counter_global.set(app.state.counter_global.get() + pt.Int(1)),
        # We now set the return value
        output.set(app.state.counter_global.get())
    )

@app.external
# This method reduces the count
def decrement_global(*, output: pt.abi.Uint64) -> pt.Expr:
    return pt.Seq(
        # save the state value counter_global as counter - 1
        app.state.counter_global.set(app.state.counter_global.get() - pt.Int(1)),
        # return the value
        output.set(app.state.counter_global.get())
    )

