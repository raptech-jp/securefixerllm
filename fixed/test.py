
from jinja2 import Template
from flask import request, Flask

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def home():
    name = request.args.get('name', 'Guest')
    renderer = Template('Hello, {{ name }}')
    return renderer.render(name=name)

if __name__ == "__main__":
    app.run()
