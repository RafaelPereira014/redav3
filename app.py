import math
from flask import Flask, render_template, request
import mysql.connector
from db_operations.resources import *
from db_operations.apps import *
from db_operations.tools import *
from db_operations.resources_details import *
from db_operations.users_op import *
from db_operations.scripts import *



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
    
    for resource in recent_resources:
        resource['image_url'] = get_resource_image_url(resource['slug'])
        resource['embed'] = get_resource_embed(resource['id'])
    highlighted_resources = get_highlighted_resources()  # Corrected variable name
    return render_template('index.html', recent_resources=recent_resources, highlighted_resources=highlighted_resources)


@app.route('/resources')
def resources():
    search_term = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12

    if search_term:
        # If search term is provided, search for resources
        paginated_resources, total_resources = search_resources(search_term, page, per_page)
    else:
        # Otherwise, fetch all resources
        paginated_resources = get_all_resources(page, per_page)
        total_resources = get_total_resource_count()

    total_pages = (total_resources + per_page - 1) // per_page

    for resource in paginated_resources:
        resource['image_url'] = get_resource_image_url(resource['slug'])
        resource['embed'] = get_resource_embed(resource['id'])
        resource['details'] = get_combined_details(resource['id'])  # Fetch resource details

    # Define the range of pages to show
    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    else:
        if page <= 3:
            page_range = range(1, 6)
        elif page >= total_pages - 2:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(page - 2, page + 3)

    return render_template('resources.html', all_resources=paginated_resources, page=page, total_pages=total_pages, page_range=page_range, search_term=search_term)


@app.route('/resources/search')
def search():
    search_term = request.args.get('search')
    page = int(request.args.get('page', 1))
    per_page = 10  # Number of resources per page

    resources = []
    total_results = 0
    if search_term:
        resources, total_results = search_resources(search_term, page, per_page)

    total_pages = math.ceil(total_results / per_page)
    page_range = range(1, total_pages + 1)

    return render_template(
        'resources.html',
        all_resources=resources,
        page=page,
        total_pages=total_pages,
        page_range=page_range
    )


@app.route('/resources/details/<int:resource_id>')
def resource_details(resource_id):
    resource_details = get_combined_details(resource_id)
    
    if not resource_details:
        return render_template('error.html', message='Resource not found'), 404
    
    slug = get_resouce_slug(resource_id)
    resource_details['image_url'] = get_resource_image_url(slug)
    resource_details['embed'] = get_resource_embed(resource_id)
    resource_details['files'] = get_resource_files(slug)
    resource_details['link'] = get_resource_link(resource_id)
    resource_details['operations'] = get_propostasOp(resource_id)  # Fetching operations
    
    related_resources = get_related_resources(resource_details['title'])
    for related in related_resources:
        related_slug = get_resouce_slug(related['id'])
        related['image_url'] = get_resource_image_url(related_slug)
        related['embed'] = get_resource_embed(related['id'])
    
    return render_template('resource_details.html', resource_details=resource_details, related_resources=related_resources)




# Edit resources
@app.route('/resources/edit/<int:resource_id>')
def resource_edit(resource_id):
    resource_details = get_combined_details(resource_id)
    
    if not resource_details:
        return render_template('error.html', message='Resource not found'), 404
    
    related_resources = get_related_resources(resource_details['title'])
    
    return render_template('edit_resource.html', resource_details=resource_details, related_resources=related_resources)


@app.route('/apps', methods=['GET'])
def apps():
    page = request.args.get('page', default=1, type=int)
    apps_per_page = 12

    # Fetch apps for the current page
    paginated_apps = get_all_apps(page, apps_per_page)
    
    # Fetch total app count for pagination
    total_apps = get_total_app_count()
    total_pages = (total_apps + apps_per_page - 1) // apps_per_page

    # Update each app with its slug and image URL
    for app in paginated_apps:
        app['slug'] = get_app_slug(app['id'])
        app['metadados']=get_app_metadata(app['id'])
        if app['slug']:
            app['image_url'] = get_apps_image_url(app['slug'])
        else:
            app['image_url'] = None
    
   

    # Define the range of pages to show
    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    else:
        if page <= 3:
            page_range = range(1, 6)
        elif page >= total_pages - 2:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(page - 2, page + 3)

    return render_template('apps.html', all_apps=paginated_apps, page=page, total_pages=total_pages, page_range=page_range)




@app.route('/novaapp')
def novaapp():
    return render_template('novaapp.html')

# Tools
@app.route('/tools')
def tools():
    page = request.args.get('page', 1, type=int)
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

    # Define the range of pages to show
    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    else:
        if page <= 3:
            page_range = range(1, 6)
        elif page >= total_pages - 2:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(page - 2, page + 3)

    return render_template('tools.html', all_tools=all_tools, page=page, total_pages=total_pages, page_range=page_range)



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
    apps_user,apps_count = get_apps_from_user(userid)
    tools_user, tools_count = get_tools_from_user(userid)
    user_details = get_details(userid)
    resources_count=no_resources(userid)
    scripts_user,scripts_count=get_script_details(userid)
    
    return render_template('my_account.html', my_resources=my_resources,apps_count=apps_count,apps_user=apps_user, tools_user=tools_user,tools_count=tools_count,user_details=user_details,resources_count=resources_count,scripts_user=scripts_user,scripts_count=scripts_count)


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
