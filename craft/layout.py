import dash_core_components as dcc
import dash_html_components as html
from .utils import construct_variable_definer

functions = "mx-1 my-2 p-2 flex justify-between"
input_class = "px-2 py-1 ml-2 bg-indigo-100 rounded-md"


def feather_icon(name: str):
    return html.I(**{"data-feather": name})


layout = html.Div(className="flex container justify-between mx-6 my-4 max-h-screen", children=[
    html.Div(children=[
        html.H1(className="text-3xl font-bold", children="System Observer"),
        html.Div(className="px-8 mt-5", children=html.Img(src="/assets/system.png", alt="system graph")),
        html.H2(className="text-xl mt-3 font-bold", children="System"),
        html.Div(children=[
            html.Div(className=functions, children=[
                html.Span(className="text-md", children="Plant"),
                dcc.Input(id="plant_raw", className=input_class, value="1/(s+3)"),
            ])
        ]),
        html.Div(children=[
            html.Div(className=functions, children=[
                html.Span(className="text-md", children="Controller"),
                dcc.Input(id="controller_raw", className=input_class, value="1"),
            ])
        ]),
        html.Div(children=[
            html.Div(className=functions, children=[
                html.Span(className="text-md", children="Feedback"),
                dcc.Input(id="feedback_raw", className=input_class, value="1"),
            ])
        ]),
        html.H2(className="text-xl mt-8 mb-3 font-bold", children="Variable"),
        html.Div(id="var-x-container", className="w-auto",
                 children=construct_variable_definer("range", "x", values=[0, 5, 1])),
    ]),
    html.Div(className="relative max-h-full", children=[
        html.Button(id="compute-btn", className="z-10", children=[feather_icon("play"), "compute"]),
    ]),
    html.Div(className="max-h-full px-0 ml-auto", children=[
        dcc.Graph(id="time-plot"),
        dcc.Graph(id="freq-mag-plot"),
        dcc.Graph(id="freq-phase-plot")
    ]),
])
