from flask import Flask, render_template

app = Flask(__name__)

# Homepage
@app.route('/')
def homepage():
    return render_template('index.html')

# Resources
@app.route('/resources')
def resources():
    return render_template('resources.html')

# Resource Details
@app.route('/resources/details')
def resource_details():
    return render_template('resource_details.html')

# Apps
@app.route('/apps')
def apps():
    return render_template('apps.html')

@app.route('/novaapp')
def novaapp():
    return render_template('novaapp.html')

# Tools
@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/novaferramenta')
def newtool():
    return render_template('novaferramenta.html')

# My Account
@app.route('/myaccount')
def my_account():
    return render_template('my_account.html')

# New_resource
@app.route('/novorecurso')
def novo_recurso():
    return render_template('new_resource.html')

@app.route('/novorecurso2')
def novo_recurso2():
    return render_template('new_resource2.html')

# about page
@app.route('/sobre')
def about():
    return render_template('sobre.html')


# Admin Page
@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == "__main__":
    app.run(debug=True)
