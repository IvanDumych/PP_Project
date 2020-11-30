from pp_project import app


@app.route('/')
@app.route('/api/v1/hello-world-7')
def index():
    return 'Hello World-3'
