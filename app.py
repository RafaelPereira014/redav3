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

########---------------------------------_################
# Admin Page
@app.route('/dashboard')
def admin():
    return render_template('admin/admin.html')

@app.route('/dashboard/recursos/pendentes')
def rec_pendentes():
    return render_template('admin/recursos/pendentes.html')

@app.route('/dashboard/recursos/po/pendentes')
def po_pendentes():
    return render_template('admin/recursos/po_pendentes.html')

@app.route('/dashboard/aplicacoes')
def admin_apps():
    return render_template('admin/aplicacoes/aplicacoes.html')

@app.route('/dashboard/aplicacoes/pendentes')
def admin_apps_pendentes():
    return render_template('admin/aplicacoes/pendentes.html')

@app.route('/dashboard/ferramentas')
def admin_tools():
    return render_template('admin/ferramentas/ferramentas.html')

@app.route('/dashboard/ferramentas/pendentes')
def admin_tools_pendentes():
    return render_template('admin/ferramentas/pendentes.html')

@app.route('/dashboard/comentarios/pendentes')
def admin_comments():
    return render_template('admin/comentarios/pendentes.html')

@app.route('/dashboard/comentarios/palavras-proibidas')
def admin_comments_prohi():
    return render_template('admin/comentarios/palavras-proibidas.html')

@app.route('/dashboard/taxonomias')
def admin_taxonomies():
    return render_template('admin/taxonomias/taxonomias.html')

@app.route('/dashboard/taxonomias/relacoes')
def admin_taxonomies_rel():
    return render_template('admin/taxonomias/relacoes.html')

@app.route('/dashboard/utilizadores')
def admin_users():
    return render_template('admin/utilizadoes/utilizadores.html')









if __name__ == "__main__":
    app.run(debug=True)
