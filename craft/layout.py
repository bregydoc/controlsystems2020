import dash_core_components as dcc
import dash_html_components as html


def icon(name: str):
    return html.I(**{"data-feather": name})


layout = html.Div(className="flex container justify-between mx-auto", children=[
    html.Div(children="left"),
    html.Div(children=[
        html.Button(children=icon("circle")),
    ]),
    html.Div(children="right"),
])