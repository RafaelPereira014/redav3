from flask import Flask, render_template, request
import mysql.connector
from db_operations.resources import *
from db_operations.apps import *



app = Flask(__name__)


config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'passroot',
    'database': 'redav3'
}

connection = mysql.connector.connect(**config)

# Homepage
@app.route('/')
def homepage():
    recent_resources = get_recent_approved_resources()
    return render_template('index.html',recent_resources=recent_resources)

# Resources
@app.route('/resources')
def resources():
    all_resources = get_all_resources()
    # Pagination settings
    page = request.args.get('page', 1, type=int)
    per_page = 12
    total_resources = len(all_resources)
    total_pages = (total_resources + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_resources = all_resources[start:end]
    
    return render_template('resources.html', all_resources=paginated_resources, page=page, total_pages=total_pages)
# Resource Details
@app.route('/resources/details')
def resource_details():
    return render_template('resource_details.html')

# Apps
@app.route('/apps', methods=['GET'])
def apps():
    all_apps = get_all_apps()  # Replace with your function to get all apps
    page = request.args.get('page', default=1, type=int)
    apps_per_page = 8
    total_apps = len(all_apps)
    total_pages = (total_apps + apps_per_page - 1) // apps_per_page
    
    start_index = (page - 1) * apps_per_page
    end_index = min(start_index + apps_per_page, total_apps)
    
    apps_for_current_page = all_apps[start_index:end_index]
    
    return render_template('apps.html', all_apps=apps_for_current_page, total_pages=total_pages, current_page=page)


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

# privacy page 
@app.route('/politica-privacidade')
def privacy():
    return render_template('privacy.html')

# help page

@app.route('/ajuda')
def help():
    return render_template('help.html')

# fale connosco

@app.route('/faleconnosco')
def speakwus():
    return render_template('faleconnosco.html')





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

@app.route('/dashboard/recursos/ocultos')
def hidden():
    return render_template('admin/recursos/ocultos.html')

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

#######----- taxonomias-----------####
@app.route('/dashboard/taxonomias')
def admin_taxonomies():
    return render_template('admin/taxonomias/taxonomias.html')

@app.route('/dashboard/taxonomias/nome_taxonomia')
def admin_edit_taxonomies():
    return render_template('admin/taxonomias/edit_taxonomia.html')

@app.route('/dashboard/taxonomias/relacoes')
def admin_taxonomies_rel():
    return render_template('admin/taxonomias/relacoes.html')

#######----------------####
@app.route('/dashboard/utilizadores')
def admin_users():
    return render_template('admin/utilizadores/utilizadores.html')












if __name__ == "__main__":
    app.run(debug=True)
