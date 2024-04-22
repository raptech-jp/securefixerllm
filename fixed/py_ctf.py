
import os
from flask import Flask, render_template, request, url_for, redirect, session, render_template_string
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

@app.route('/golem', methods=['GET', 'POST'])
def golem():
    if request.method != 'POST':
        return redirect(url_for('index'))
    
    golem = request.form.get('golem', None)
    if golem is not None:
        golem = golem.replace('.', '').replace('_', '').replace('{', '').replace('}', '')
        
    if 'golem' not in session or session['golem'] is None:
        session['golem'] = golem

    template = None
    if session['golem'] is not None:
        template = f"""
{{% extends "layout.html" %}}
    {{% block body %}}
        <h1>Golem Name</h1>
        <div class="row">
            <div class="col-md-6 col-md-offset-3 center">
                Hello: {session['golem']}, why don't you look at our <a href='/article?name=article'>article</a>?
            </div>
        </div>
    {{% endblock %}}
"""
        session['golem'] = None

    return render_template_string(template)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/article', methods=['GET'])
def article():
    error = 0
    if 'name' in request.args:
        page = request.args.get('name')
    else:
        page = 'article'

    if 'flag' in page:
        page = 'notallowed.txt'
    
    try:
        with open(f'/home/golem/articles/{page}') as file:
            template = file.read()
    except Exception as e:
        template = str(e)

    return render_template('article.html', template=template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
