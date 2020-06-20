index_template = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
    <script>feather.replace()</script>
</html>

'''

renderer = '''
var renderer = new DashRenderer({
    request_pre: (payload) => {
        // print out payload parameter
        console.log("pre:", payload);
    },
    request_post: (payload, response) => {
        // print out payload and response parameter
        console.log("post_a:", payload);
        console.log("post_b:", response);
    }
})
'''