from flask import Flask, render_template, request
import mysql.connector
from db_operations.resources import *
from db_operations.apps import *
from db_operations.tools import *
from db_operations.resources_details import *



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
    highlighted_resources = get_highlighted_resources()  # Corrected variable name
    return render_template('index.html', recent_resources=recent_resources, highlighted_resources=highlighted_resources)


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
@app.route('/resources/details/<int:resource_id>')
def resource_details(resource_id):
    resource_details = get_combined_details(resource_id)
    if not resource_details:
        return render_template('error.html', message='Resource not found'), 404

    return render_template('resource_details.html', resource_details=resource_details)

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
def tools(page=1):
    per_page = 8
    offset = (page - 1) * per_page
    
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    # Count total number of tools for pagination
    cursor.execute("SELECT COUNT(*) as total FROM Resources WHERE type_id=%s", (1,))
    total_tools = cursor.fetchone()['total']
    
    # Fetch tools for the current page
    cursor.execute("SELECT * FROM Resources WHERE type_id=%s ORDER BY id DESC LIMIT %s OFFSET %s", (1, per_page, offset))
    all_tools = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Calculate total number of pages
    total_pages = (total_tools + per_page - 1) // per_page
    
    return render_template('tools.html', all_tools=all_tools, page=page, total_pages=total_pages)


@app.route('/novaferramenta')
def newtool():
    return render_template('novaferramenta.html')

# My Account
@app.route('/myaccount')
def my_account():
    userid = '5'
    if userid is None:
        return "User not found", 404
    
    my_resources = get_resources_from_user(userid)
    my_apps = get_apps_from_user(userid)
    my_tools = get_tools_from_user(userid)
    
    return render_template('my_account.html', my_resources=my_resources, my_apps=my_apps, my_tools=my_tools)


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
    recursos_pendentes = get_pendent_resources()
    return render_template('admin/recursos/pendentes.html',recursos_pendentes=recursos_pendentes)

@app.route('/dashboard/recursos/po/pendentes')
def po_pendentes():
    return render_template('admin/recursos/po_pendentes.html')

@app.route('/dashboard/recursos/ocultos')
def hidden():
    ocultos = get_hidden_resources()
    return render_template('admin/recursos/ocultos.html',ocultos=ocultos)

@app.route('/dashboard/aplicacoes')
def admin_apps():
    all_apps = get_apps()  # Replace with your function to get all apps
    return render_template('admin/aplicacoes/aplicacoes.html',all_apps=all_apps)

@app.route('/dashboard/aplicacoes/pendentes')
def admin_apps_pendentes():
    pendent_apps = get_pendent_apps()
    return render_template('admin/aplicacoes/pendentes.html',pendent_apps=pendent_apps)

@app.route('/dashboard/ferramentas')
def admin_tools():
    all_tools = get_all_tools()
    return render_template('admin/ferramentas/ferramentas.html',all_tools=all_tools)

@app.route('/dashboard/ferramentas/pendentes')
def admin_tools_pendentes():
    pendent_tools = get_pendent_tools()
    return render_template('admin/ferramentas/pendentes.html',pendent_tools=pendent_tools)

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
