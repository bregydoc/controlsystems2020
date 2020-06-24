import dash
import control as ct
from dash.dependencies import Input, Output, State

from craft.labo import BasicExperiment, BasicSystem, Variable
from craft.layout import layout, construct_variable_definer, state_to_variable
from craft.templates import index_template

P = ct.TransferFunction([1], [1, 1, 1])
exp = BasicExperiment(BasicSystem(P))
exp.add_variable(Variable("x", kind="range", start=0, end=5, step=1))

external_stylesheets = [
    "https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css"
]

external_scripts = [
    "https://unpkg.com/feather-icons",
    "https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
)

app.index_string = index_template
app.layout = layout


# app.renderer = renderer

@app.callback(Output("time-plot", "figure"),
              [Input("compute-btn", "n_clicks")],
              [State("plant_raw", "value"),
               State("controller_raw", "value"),
               State("feedback_raw", "value"),
               State("var-x-container", "children")])
def render_time(clicks, plant_raw, controller_raw, feedback_raw, current_var):
    fig = exp.render_step(g=plant_raw, k=controller_raw, h=feedback_raw)
    return fig


@app.callback([Output("freq-mag-plot", "figure"),
               Output("freq-phase-plot", "figure")],
              [Input("compute-btn", "n_clicks")],
              [State("plant_raw", "value"),
               State("controller_raw", "value"),
               State("feedback_raw", "value"),
               State("var-x-container", "children")])
def render_freq(clicks, plant_raw, controller_raw, feedback_raw, current_var):
    fig = exp.render_bode(g=plant_raw, k=controller_raw, h=feedback_raw)
    return fig


@app.callback(Output("var-x-container", "children"),
              [Input("var-kind-select", "value"),
               Input("var-name", "value")],
              [State("var-x-container", "children")])
def update_variable_params(kind, name, current_var):
    if name != "":
        var = state_to_variable(current_var)
        current_kind = var.kind

        current_once = var.fixed or 0.0
        current_array = var.fixed or [0.0]
        current_start = var.start or 0.0
        current_end = var.end or 1.0
        current_step = var.step or 1.0

        if kind == current_kind:
            if kind == "once":
                current_var = construct_variable_definer(kind, name, [current_once])
            elif kind == "array":
                current_var = construct_variable_definer(kind, name, current_array)
            elif kind == "range":
                current_var = construct_variable_definer(kind, name, [current_start, current_end, current_step])
        else:
            current_var = construct_variable_definer(kind, name)

        exp.update_var(name, var)
    return current_var


if __name__ == '__main__':
    app.run_server(debug=True)
