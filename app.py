from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/api/v1/hello-world-7')
def index():
    return 'Hello World-3'


if __name__ == "__main__":
    app.run()
