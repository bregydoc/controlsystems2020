import dash_core_components as dcc
import dash_html_components as html
import dash_editor_components

from .utils import construct_variable_definer
from .templates import code_start

functions = "mx-1 my-2 p-2 flex justify-between"
input_class = "px-2 py-1 ml-2 w-1/2 bg-indigo-100 rounded-md"


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
                dcc.Input(id="controller_raw", className=input_class, value="(s+2*x)/(s+4)"),
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
                 children=construct_variable_definer("range", "x", values=[1.0, 2.5, 0.5])),
        html.H2(className="text-xl mt-8 mb-3 font-bold", children=[
            html.Div(className="flex align-middle",
                     children=["Code",
                               html.Button(id="execute-btn",
                                           className="ml-auto px-2 py-1 text-base rounded-md bg-purple-300",
                                           children="Execute")
                               ])
        ]),
        html.Div(id="code-container", className="w-auto",
                 children=[dash_editor_components.PythonEditor(id='code', value=code_start)]),
        dcc.Textarea(id="code-output-exec",
                     className="flex flex-col w-full h-24 p-2 bg-gray-300",
                     readOnly=True)
    ]),
    html.Div(className="relative max-h-full", children=[
        html.Button(id="compute-btn",
                    className="mt-4 px-2 py-1 rounded-md bg-green-200 flex flex-col items-center",
                    children=[html.Div(feather_icon("play")), html.Span("Compute")]),
    ]),
    html.Div(className="max-h-full px-0 ml-auto", children=[
        dcc.Graph(id="time-plot"),
        dcc.Graph(id="freq-mag-plot"),
        dcc.Graph(id="freq-phase-plot")
    ]),
])
