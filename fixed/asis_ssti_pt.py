
import os
from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session

app = Flask(__name__)

# Simulated loading of key and flag
# Normally would be from a configuration or environment variable
app.secret_key = 'secret_key_here'
FLAG = 'flag_here'

@app.route('/golem', methods=['GET', 'POST'])
def golem():
    if request.method != 'POST':
        return redirect(url_for('index'))
    
    golem = request.form.get('golem')
    if golem is not None:
        golem = golem.replace('.', '').replace('_', '').replace('{', '').replace('}', '')
    
    if 'golem' not in session or session['golem'] is None:
        session['golem'] = golem
    
    template = None
    if session['golem'] is not None:
        template = """{% extends "layout.html" %}
\t\t{% block body %}
\t\t<h1>Golem Name</h1>
\t\t<div class="row">
\t\t<div class="col-md-6 col-md-offset-3 center">
\t\tHello: {}, why don't you look at our <a href='/article?name=article'>article</a>?
\t\t</div>
\t\t</div>
\t\t{% endblock %}
\t\t"""
        template = template.format(session['golem'])
        session['golem'] = None
    
    return render_template_string(template)

@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')

@app.route('/article', methods=['GET'])
def article():
    name = request.args.get('name', 'default')
    page = 'notallowed.txt' if 'flag' in name else name
    try:
        with open(f'/home/golem/articles/{page}') as file:
            template = file.read()
    except Exception as e:
        template = str(e)
    
    return render_template('article.html', template=template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
