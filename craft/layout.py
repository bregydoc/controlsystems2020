import dash_core_components as dcc
import dash_html_components as html
from typing import Dict
from dash.development.base_component import Component
from craft.labo import Variable

functions = "mx-1 my-2 p-2 flex justify-between"
input_class = "px-2 py-1 ml-2 bg-indigo-100 rounded-md"


def feather_icon(name: str):
    return html.I(**{"data-feather": name})


def construct_variable_definer(kind: str, name: str, values: list = None) -> Component:
    inputs = []
    if kind == "once":
        inputs = [
            dcc.Input(
                id="var-input-once",
                className=input_class,  # +" w-1/3",
                value=str(values[0]) if values is not None and len(values) > 0 else None
            )
        ]

    if kind == "array":
        inputs = [
            dcc.Input(
                id="var-input-array",
                className=input_class,  # +" w-1/3",
                value=str(values) if values is not None and len(values) > 0 else None
            )
        ]

    if kind == "range":
        inputs = [
            dcc.Input(
                id="var-input-start",
                className=input_class + " w-1/12",
                value=str(values[0]) if values is not None and len(values) > 2 else None
            ),
            dcc.Input(
                id="var-input-end",
                className=input_class + " w-1/12",
                value=str(values[1]) if values is not None and len(values) > 2 else None
            ),
            dcc.Input(
                id="var-input-step",
                className=input_class + " w-1/12",
                value=str(values[2]) if values is not None and len(values) > 2 else None
            )
        ]

    return html.Div(className="flex w-full mb-3", children=[
        dcc.Input(id="var-name", className="px-2 py-1 mr-2 bg-indigo-100 rounded-md w-2/12", value=name),
        dcc.Dropdown(
            id='var-kind-select',
            className="w-32",
            options=[
                {'label': 'Once', 'value': 'once'},
                {'label': 'Array', 'value': 'array'},
                {'label': 'Range', 'value': 'range'}
            ],
            clearable=False,
            value=kind
        ),
        *inputs
    ])


def state_to_variable(current_var: Dict) -> Variable:
    current_kind = ""
    current_once = None
    current_array = None
    current_start = None
    current_end = None
    current_step = None
    for child in current_var["props"]["children"]:
        if child["props"]["id"] == "var-kind-select":
            current_kind = child["props"]["value"]

    if current_kind == "once":
        once = [child["props"]["value"] for child in current_var["props"]["children"]
                if child["props"]["id"] == "var-input-once"]
        current_once = float(once[0]) if len(once) > 0 else None

    if current_kind == "array":
        array = [child["props"]["value"] for child in current_var["props"]["children"]
                 if child["props"]["id"] == "var-input-array"]
        current_array = exec(array[0]) if len(array) > 0 else None

    if current_kind == "range":
        start = [child["props"]["value"] for child in current_var["props"]["children"]
                 if child["props"]["id"] == "var-input-start"]
        end = [child["props"]["value"] for child in current_var["props"]["children"]
               if child["props"]["id"] == "var-input-end"]
        step = [child["props"]["value"] for child in current_var["props"]["children"]
                if child["props"]["id"] == "var-input-step"]

        current_start = float(start[0]) if len(start) > 0 else None
        current_end = float(end[0]) if len(end) > 0 else None
        current_step = float(step[0]) if len(step) > 0 else None

    # defaults
    current_once = current_once or 0.0
    current_array = current_array or [0.0]
    current_start = current_start or 0.0
    current_end = current_end or 1.0
    current_step = current_step or 1.0

    name = [child["props"]["value"] for child in current_var["props"]["children"]
            if child["props"]["id"] == "var-name"]

    current_name = str(name[0]) if len(name) > 0 else ""

    if current_kind == "once":
        current_var = Variable(current_name, current_kind, fixed=current_once)
    elif current_kind == "array":
        current_var = Variable(current_name, current_kind, fixed=current_array)
    elif current_kind == "range":
        current_var = Variable(current_name, current_kind, start=current_start, end=current_end, step=current_step)

    return current_var


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
        # html.Div(className="w-full flex justify-center", children=[
        #     html.Button(id="add-new-var", className="px-4 py-1 mt-8 bg-indigo-300 rounded-md", children="Add Var")
        # ])
    ]),
    html.Div(className="relative max-h-full", children=[
        html.Button(id="compute-btn", className="z-10", children=feather_icon("play")),
    ]),
    html.Div(className="max-h-full px-0 ml-auto", children=[
        dcc.Graph(id="time-plot"),
        dcc.Graph(id="freq-mag-plot"),
        dcc.Graph(id="freq-phase-plot")
    ]),
])
