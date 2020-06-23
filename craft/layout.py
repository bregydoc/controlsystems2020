import dash_core_components as dcc
import dash_html_components as html


functions = "mx-1 my-2 p-2 flex justify-between"
input_class = "px-2 py-1 ml-2 bg-indigo-100 rounded-md"


def feather_icon(name: str):
    return html.I(**{"data-feather": name})


def construct_variable_definer(kind: str, name: str, values: list = None):
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
            id='var-select',
            className="w-32",
            options=[
                {'label': 'Once', 'value': 'once'},
                {'label': 'Array', 'value': 'array'},
                {'label': 'Range', 'value': 'range'}
            ],
            value=kind
        ),
        *inputs
    ])


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
        html.Div(id="var-x-container", className="w-auto"),
        html.Div(className="w-full flex justify-center", children=[
            html.Button(id="add-new-var", className="px-4 py-1 mt-8 bg-indigo-300 rounded-md", children="Add Var")
        ])
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