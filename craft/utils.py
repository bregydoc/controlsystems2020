import dash_core_components as dcc
import dash_html_components as html
from typing import Dict
from dash.development.base_component import Component
from .labo import Variable
import ast

input_class = "px-2 py-1 ml-2 bg-indigo-100 rounded-md"


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

    return html.Div(id="var-mods", className="flex w-full mb-3", children=[
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
        current_array = ast.literal_eval(array[0]) if len(array) > 0 else None

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

    print(current_once, current_array, current_start)
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

