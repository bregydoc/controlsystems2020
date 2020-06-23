import dash
import dash_core_components as dcc
import dash_html_components as html
import control as ct
import control2020 as ct20
import sympy as sp
from dash.dependencies import Input, Output, State

from labo import BasicExperiment, BasicSystem
from layout import layout, construct_variable_definer
from templates import renderer, index_template

P = ct.TransferFunction([1], [1, 1, 1])
exp = BasicExperiment(BasicSystem(P))

external_stylesheets = [
    'https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css'
]

external_scripts = [
    'https://unpkg.com/feather-icons',
    'https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js'
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
               State("feedback_raw", "value")])
def render_time(clicks, plant_raw, controller_raw, feedback_raw):
    exp.system.update(g=plant_raw, k=controller_raw, h=feedback_raw)
    fig = exp.render_step()
    return fig


@app.callback([Output("freq-mag-plot", "figure"),
               Output("freq-phase-plot", "figure")],
              [Input("compute-btn", "n_clicks")])
def render_freq(clicks):
    fig = exp.render_bode()
    return fig


@app.callback(Output("vars-container", "children"),
              [Input("add-new-var", "n_clicks")],
              [State("vars-container", "children")])
def create_new_var(clicks, current_vars):
    print(clicks)
    print(len(current_vars))
    new_var = construct_variable_definer("once", "x")
    current_vars.append(new_var)
    return current_vars


if __name__ == '__main__':
    app.run_server(debug=True)
