from itertools import islice
import math
import bcrypt
import re
from flask import Flask, flash, jsonify, redirect, render_template, request
from markupsafe import Markup
import mysql.connector
from db_operations.resources import *
from db_operations.apps import *
from db_operations.tools import *
from db_operations.resources_details import *
from db_operations.users_op import *
from db_operations.scripts import *
from db_operations.admin import *
from db_operations.new_resource import *
from db_operations.user import *
from db_operations.new_operations import *



app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Needed for session management


config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'passroot',
    'database': 'redav4'
}

connection = mysql.connector.connect(**config)



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')
        
        
        if not email or not password:
            error = 'Username and password are required'
            return render_template('login.html', error=error)

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id, role_id, password FROM Users WHERE email = %s", (email,))
        user_data = cursor.fetchone()  # Fetch the user ID, type, and hashed password from the database
        cursor.close()
        
        if user_data:
            stored_password = user_data[2].encode('utf-8')  # Ensure stored password is encoded as bytes
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                session['user_id'] = user_data[0]  # Store user ID in session
                session['user_type'] = user_data[1]  # Store user type in session
                return redirect('/')  # Redirect to dashboard or another page upon successful login
            else:
                error = 'Invalid username or password'
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/register')
def register():
    
    return render_template('register.html')

def user_logged_in():
    return 'user_id' in session  # Modify this based on your session setup

@app.route('/')
def homepage():
    recent_resources = get_recent_approved_resources()
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)

    # Modify recent_resources to include image_url and embed
    for resource in recent_resources:
        resource['image_url'] = get_resource_image_url(resource['slug'])
        resource['embed'] = get_resource_embed(resource['id'])
        resource['details'] = get_combined_details(resource['id'])  # Fetch resource details


    highlighted_resources = get_highlighted_resources()

    return render_template('index.html', recent_resources=recent_resources, highlighted_resources=highlighted_resources, admin=admin)


@app.template_filter('strip_html')
def strip_html_filter(text):
    """Remove HTML tags from a string."""
    return strip_html_tags(text)

app.jinja_env.filters['strip_html'] = strip_html_filter


@app.route('/resources')
def resources():
    search_term = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)

    if search_term:
        # If search term is provided, search for resources
        paginated_resources, total_resources = search_resources(search_term, page, per_page)
    else:
        # Otherwise, fetch all resources
        paginated_resources = get_all_resources(page, per_page)
        total_resources = get_total_resource_count()

    total_pages = (total_resources + per_page - 1) // per_page
    total_resources = get_total_resource_count()

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

    return render_template('resources.html', all_resources=paginated_resources, page=page, total_pages=total_pages, page_range=page_range, search_term=search_term, admin=admin,total_resources=total_resources)





@app.route('/resources/details/<int:resource_id>')
def resource_details(resource_id):
    combined_details = get_combined_details(resource_id)
    slug= get_resouce_slug(resource_id)

   
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)
   

    # Extract combined details
    resource_details = combined_details

    # Fetch and append additional details
    slug = get_resouce_slug(resource_id)
    resource_details['image_url'] = get_resource_image_url(slug)
    resource_details['embed'] = get_resource_embed(resource_id)
    resource_details['files'] = get_resource_files(slug)
    resource_details['link'] = get_resource_link(resource_id)
    resource_details['operations'] = get_propostasOp(resource_id)  # Fetching operations
    resource_details['username'] = get_username(resource_details['user_id'])

    # Fetch related resources and append additional details
    related_resources = get_related_resources(resource_details['title'])
    for related in related_resources:
        related_combined_details = get_combined_details(related['id'])
        if related_combined_details:
            related.update(related_combined_details)
            related_slug = get_resouce_slug(related['id'])
            related['image_url'] = get_resource_image_url(related_slug)
            related['embed'] = get_resource_embed(related['id'])
            related['files'] = get_resource_files(related_slug)
            related['link'] = get_resource_link(related['id'])
            related['operations'] = get_propostasOp(related['id'])
            related['username'] = get_username(related_combined_details['user_id'])

    return render_template('resource_details.html', 
                           resource_details=resource_details, 
                           related_resources=related_resources, 
                           admin=admin,slug=slug)

@app.route('/hide_resource/<int:resource_id>', methods=['POST'])
def hide_resource_route(resource_id):
    result = hide_resource(resource_id)
    return result

@app.route('/delete_resource/<int:resource_id>', methods=['POST'])
def delete_resource_route(resource_id):
    result = delete_resource(resource_id)
    return result

@app.route('/gerirpropostas/<slug>')
def gerir_propostas(slug):
    
    return render_template('gerirpropostas.html')


@app.route('/novaproposta/<slug>', methods=['GET', 'POST'])
def nova_proposta(slug):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)
    anos = get_unique_terms(level=1)
    resource_id = get_resouce_id(slug)
    
    ano = request.args.get('ano')
    dominios = []
    subdominios = []
    conceitos = []
    
    disciplinas = get_filtered_terms(level=2, parent_level=1, parent_term=ano) if ano else []
    for disciplina in disciplinas:
        dominios = get_filtered_terms(level=3, parent_level=2, parent_term=disciplina) if ano else []
        for dominio in dominios:
            subdominios = get_filtered_terms(level=4, parent_level=3, parent_term=dominio) if ano else []
            for subdominio in subdominios:
                conceitos = get_filtered_terms(level=5, parent_level=4, parent_term=subdominio) if ano else []

    if request.method == 'POST':
        data = request.form
        selected_anos = list(set(data.getlist('anos')))  # Use set to remove duplicates
        selected_disciplinas = list(set(data.getlist('disciplinas')))  # Use set to remove duplicates
        selected_dominios = list(set(data.getlist('dominios')))  # Use set to remove duplicates
        selected_subdominios = list(set(data.getlist('subdominios')))  # Use set to remove duplicates
        selected_conceitos = list(set(data.getlist('conceitos')))  # Use set to remove duplicates
        outros_conceitos = data.get('outros_conceitos', '')
        descricao = data.get('descricao', '')
        
        insert_script(resource_id, user_id, selected_anos, selected_disciplinas, selected_dominios, selected_subdominios, selected_conceitos, descricao)
        conn.commit()
    
        # Optionally, you can return a JSON response indicating success
        return jsonify({'message': 'Proposta adicionada com sucesso!'})

    conn.close()
    cursor.close()

    return render_template('novaproposta.html', anos=anos, disciplinas=disciplinas, dominios=dominios, subdominios=subdominios, admin=admin, conceitos=conceitos, slug=slug,resource_id=resource_id)





@app.route('/resources/edit/<int:resource_id>', methods=['GET', 'POST'])
def resource_edit(resource_id):
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)
    resource_details = get_combined_details(resource_id)
    formatos = get_formatos()
    use_mode = get_modos_utilizacao()
    requirements = get_requisitos_tecnicos()
    idiomas = get_idiomas()

    if not resource_details:
        return render_template('error.html', message='Resource not found'), 404

    if request.method == 'POST':
        title = request.form.get('titulo') or resource_details.get('title')
        autor = request.form.get('autor') or resource_details.get('operation_author')
        org = request.form.get('organizacao') or resource_details.get('organization')
        descricao = request.form.get('descricao') or resource_details.get('description')
        idiomas_title = request.form.getlist('idiomas') or resource_details.get('idiomas_title')
        formato_title = request.form.getlist('formato') or resource_details.get('formato_title')
        modo_utilizacao_title = request.form.getlist('use_mode') or resource_details.get('modo_utilizacao_title')
        requisitos_tecnicos_title = request.form.getlist('requirements') or resource_details.get('requisitos_tecnicos_title')
        slug = generate_slug(title)
        file = request.files.get('ficheiro')

        resource_details.update({
            'title': title,
            'slug': slug,
            'description': descricao,
            'operation': 'update',
            'operation_author': autor,
            'organization': org,
            'link': request.form.get('link') or resource_details.get('link'),  # Add any other fields as needed
            'author': autor,
            'updated_at': datetime.now(),
            'user_id': user_id,
            'type_id': 2,
            'image_id': 1,
            'hidden': 0
        })

        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)

        # Update resource details
        update_resource_details(cursor, resource_id, resource_details)

        # Update taxonomy details
        taxonomy_details = {
            'Idiomas': idiomas_title,
            'Formato': formato_title,
            'Modos de utilização': modo_utilizacao_title,
            'Requisitos técnicos': requisitos_tecnicos_title,
            # Add 'Anos de escolaridade' if it's a part of your form data
        }
        

        update_taxonomy_details(cursor, resource_id, taxonomy_details)
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('resource_details', resource_id=resource_id))

    # Extract titles from resource_details
    formato_title = resource_details.get('formato_title')
    modo_utilizacao_title = resource_details.get('modo_utilizacao_title')
    req_tecnicos_title = resource_details.get('requisitos_tecnicos_title')
    idiomas_title = resource_details.get('idiomas_title')

    related_resources = get_related_resources(resource_details['title'])

    return render_template(
        'edit_resource.html',
        resource_details=resource_details,
        related_resources=related_resources,
        formatos=formatos,
        use_mode=use_mode,
        requirements=requirements,
        idiomas=idiomas,
        formato_title=formato_title,
        modo_utilizacao_title=modo_utilizacao_title,
        req_tecnicos_title=req_tecnicos_title,
        idiomas_title=idiomas_title,
        admin=admin
    )

    
@app.route('/resources/edit2/<int:resource_id>', methods=['GET', 'POST'])
def resource_edit2(resource_id):
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)
    resource_details = get_combined_details(resource_id)
    
    if request.method == 'POST':
        data = request.form
        selected_anos = list(set(data.getlist('anos')))  # Use set to remove duplicates
        selected_disciplinas = list(set(data.getlist('disciplinas')))  # Use set to remove duplicates
        selected_dominios = list(set(data.getlist('dominios')))  # Use set to remove duplicates
        selected_subdominios = list(set(data.getlist('subdominios')))  # Use set to remove duplicates
        selected_conceitos = list(set(data.getlist('conceitos')))  # Use set to remove duplicates
        descricao = data.get('descricao', '')
        
        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)

        update_script(resource_id, user_id, selected_anos, selected_disciplinas, selected_dominios, selected_subdominios, selected_conceitos, descricao)
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Proposta atualizada com sucesso!'})

    anos = get_unique_terms(level=1)
    disciplinas = get_filtered_terms(level=2, parent_level=1, parent_term=resource_details['ano'])
    dominios = get_filtered_terms(level=3, parent_level=2, parent_term=resource_details['disciplina'])
    subdominios = get_filtered_terms(level=4, parent_level=3, parent_term=resource_details['dominio'])
    conceitos = get_filtered_terms(level=5, parent_level=4, parent_term=resource_details['subdominio'])

    return render_template('edit_resource2.html', anos=anos, disciplinas=disciplinas, dominios=dominios, subdominios=subdominios, conceitos=conceitos, resource_details=resource_details, admin=admin)



@app.route('/apps', methods=['GET'])
def apps():
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)
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

    return render_template('apps.html', all_apps=paginated_apps, page=page, total_pages=total_pages, page_range=page_range,admin=admin)

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    word = data.get('word')
    results = search_apps(word)
    return jsonify(results)



@app.route('/novaapp')
def novaapp():
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)
    return render_template('novaapp.html',admin=admin)

# Tools
@app.route('/tools')
def tools():
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)
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
    
    for tool in all_tools:
        tool_id = tool['id']
        tool_metadata = get_tools_metadata(tool_id)
        tool['link'] = tool_metadata
        
        

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
            
    

    return render_template('tools.html', all_tools=all_tools, page=page, total_pages=total_pages, page_range=page_range,admin=admin)



@app.route('/novaferramenta')
def newtool():
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)
    return render_template('novaferramenta.html',admin=admin)

# My Account
@app.route('/myaccount')
def my_account():
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)
    
    my_resources = get_resources_from_user(user_id)
    apps_user, apps_count = get_apps_from_user(user_id)
    tools_user, tools_count = get_tools_from_user(user_id)
    user_details = get_details(user_id)
    resources_count = no_resources(user_id)
    scripts_user,scripts_count = get_script_details_by_user(user_id)
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    #resources
    total_resources = len(my_resources)
    total_pages = math.ceil(total_resources / per_page)
    paginated_resources = my_resources[(page - 1) * per_page:page * per_page]
    
    #proposals
    total_proposals = scripts_count
    total_pages_proposals = math.ceil(total_proposals / per_page)
    paginated_proposals = scripts_user[(page - 1) * per_page:page * per_page]
    
    return render_template(
        'my_account.html',
        my_resources=paginated_resources,
        apps_count=apps_count,
        apps_user=apps_user,
        tools_user=tools_user,
        tools_count=tools_count,
        user_details=user_details,
        resources_count=resources_count,
        scripts_user=scripts_user,
        scripts_count=scripts_count,
        page=page,
        total_pages=total_pages,
        admin=admin,
        total_pages_proposals=total_pages_proposals,
        paginated_proposals=paginated_proposals
    )


@app.route('/novorecurso', methods=['GET', 'POST'])
def novo_recurso():
    user_id = session.get('user_id')
    admin = is_admin(user_id)
    formatos = get_formatos()
    use_mode = get_modos_utilizacao()
    requirements = get_requisitos_tecnicos()
    idiomas = get_idiomas()
    anos = get_anos_escolaridade()

    if request.method == 'POST':
        title = request.form.get('titulo')
        autor = request.form.get('autor')
        org = request.form.get('organizacao')
        descricao = request.form.get('descricao')

        # Retrieving lists of selected items
        idiomas_title = request.form.getlist('idiomas')
        formato_title = request.form.getlist('formato')
        modo_utilizacao_title = request.form.getlist('use_mode')
        requisitos_tecnicos_title = request.form.getlist('requirements')
        anos_escolaridade_title = request.form.getlist('anos')
        slug = generate_slug(title)

        # Handle file upload if needed
        file = request.files.get('ficheiro')

        try:
            conn = connect_to_database()
            cursor = conn.cursor(dictionary=True)

            resource_details = {
                'title': title,
                'slug': slug,
                'description': descricao,
                'operation': 'create',
                'operation_author': autor,
                'techResources': None,
                'email': None,
                'organization': org,
                'duration': None,
                'highlight': 0,
                'exclusive': 0,
                'embed': None,
                'link': None,
                'author': autor,
                'approved': 0,
                'approvedScientific': 0,
                'approvedLinguistic': 0,
                'status': 1,
                'accepted_terms': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'deleted_at': None,
                'user_id': user_id,
                'type_id': 1,
                'image_id': 1,
                'hidden': 0
            }

            resource_id = insert_resource_details(cursor, resource_details)

            taxonomy_details = {
                'idiomas_title': idiomas_title[0] if idiomas_title else None,
                'formato_title': formato_title[0] if formato_title else None,
                'modo_utilizacao_title': modo_utilizacao_title[0] if modo_utilizacao_title else None,
                'requisitos_tecnicos_title': requisitos_tecnicos_title[0] if requisitos_tecnicos_title else None,
                'anos_escolaridade_title': anos_escolaridade_title[0] if anos_escolaridade_title else None,
                'created_at': datetime.now()
            }

            insert_taxonomy_details(cursor, resource_id, taxonomy_details)

            conn.commit()
            # Store resource_id in session
            session['resource_id'] = resource_id
            return redirect(url_for('novo_recurso2'))  # Replace with your target route

        except Exception as e:
            print(f"Error in transaction: {str(e)}")
            conn.rollback()
            raise  # Rethrow the exception for debugging purposes

        finally:
            cursor.close()
            conn.close()

    return render_template('new_resource.html', formatos=formatos, use_mode=use_mode, requirements=requirements, idiomas=idiomas, anos=anos, admin=admin)






@app.route('/novorecurso2', methods=['GET', 'POST'])
def novo_recurso2():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    user_id = session.get('user_id')  # Retrieve user ID from session
    admin = is_admin(user_id)
    anos = get_unique_terms(level=1)
    resource_id = session.get('resource_id')
    
    ano = request.args.get('ano')
    dominios = []
    subdominios = []
    conceitos = []
    
    disciplinas = get_filtered_terms(level=2, parent_level=1, parent_term=ano) if ano else []
    for disciplina in disciplinas:
        dominios = get_filtered_terms(level=3, parent_level=2, parent_term=disciplina) if ano else []
        for dominio in dominios:
            subdominios = get_filtered_terms(level=4, parent_level=3, parent_term=dominio) if ano else []
            for subdominio in subdominios:
                conceitos = get_filtered_terms(level=5, parent_level=4, parent_term=subdominio) if ano else []

    if request.method == 'POST':
        data = request.form
        selected_anos = list(set(data.getlist('anos')))  # Use set to remove duplicates
        selected_disciplinas = list(set(data.getlist('disciplinas')))  # Use set to remove duplicates
        selected_dominios = list(set(data.getlist('dominios')))  # Use set to remove duplicates
        selected_subdominios = list(set(data.getlist('subdominios')))  # Use set to remove duplicates
        selected_conceitos = list(set(data.getlist('conceitos')))  # Use set to remove duplicates
        outros_conceitos = data.get('outros_conceitos', '')
        descricao = data.get('descricao', '')
        
        insert_script(resource_id, user_id, selected_anos, selected_disciplinas, selected_dominios, selected_subdominios, selected_conceitos, descricao)
        conn.commit()
    
        return redirect(url_for('resource_details', resource_id=resource_id))  # Updated line

    conn.close()
    cursor.close()
    
    
    return render_template('new_resource2.html', anos=anos,admin=admin)

@app.route('/fetch_disciplinas')
def fetch_disciplinas():
    anos = request.args.get('ano').split(',')
    disciplinas_set = set()
    for ano in anos:
        disciplinas_set.update(get_filtered_terms(level=2, parent_level=1, parent_term=ano))
    disciplinas = list(disciplinas_set)
    return jsonify(disciplinas)


@app.route('/fetch_dominios')
def fetch_dominios():
    disciplina = request.args.get('disciplina')
    dominios = get_filtered_terms(level=3, parent_level=2, parent_term=disciplina)
    return jsonify(dominios)

@app.route('/fetch_subdominios')
def fetch_subdominios():
    dominio = request.args.get('dominio')
    subdominios = get_filtered_terms(level=4, parent_level=3, parent_term=dominio)
    return jsonify(subdominios)

@app.route('/fetch_conceitos')
def fetch_conceitos():
    subdominio = request.args.get('subdominio')
    conceitos = get_filtered_terms(level=5, parent_level=4, parent_term=subdominio)
    return jsonify(conceitos)







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
    date = datetime.now()  # Get current date and time
    active_users = get_active_month_users()
    monthly_tools = get_current_month_tools()
    monthly_apps = get_current_month_apps()
    monthly_resources = get_current_month_resources()
    monthly_users = get_current_month_users()
    return render_template('admin/admin.html', date=date,active_users=active_users,monthly_apps=monthly_apps,monthly_tools=monthly_tools,monthly_resources=monthly_resources,monthly_users=monthly_users)  # Pass date to template

@app.route('/dashboard/recursos/pendentes')
def rec_pendentes():
    recursos_pendentes = get_pendent_resources()
    return render_template('admin/recursos/pendentes.html',recursos_pendentes=recursos_pendentes)

@app.route('/update_approved_scientific/<int:resource_id>', methods=['POST'])
def update_approved_scientific(resource_id):
    result = update_approvedScientific(resource_id)
    return result

@app.route('/update_approved_linguistic/<int:resource_id>', methods=['POST'])
def update_approved_linguistic(resource_id):
    result = update_approvedLinguistic(resource_id)
    return result

@app.route('/dashboard/recursos/po/pendentes')
def po_pendentes():
    scripts, scripts_count = get_script_details_pendent()
    
    for script in scripts:
        resource_id = script['resource_id']
        script['title'] = get_title(resource_id)  # Add 'title' key to each script dictionary
        script['author'] = get_username(script['user_id'])
        script['operation'] = get_propostasOp(resource_id)
        

    return render_template('admin/recursos/po_pendentes.html', scripts=scripts, scripts_count=scripts_count)



@app.route('/dashboard/recursos/ocultos')
def hidden():
    ocultos = get_hidden_resources()
    
    return render_template('admin/recursos/ocultos.html',ocultos=ocultos)

@app.route('/resources/show/<int:resource_id>')
def show_resource_route(resource_id):
    result = show_resource(resource_id)
    flash(result)
    return redirect(url_for('hidden'))


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
    bad_words = badwords()
    return render_template('admin/comentarios/palavras-proibidas.html',bad_words=bad_words)

#######----- taxonomias-----------####
@app.route('/dashboard/taxonomias')
def admin_taxonomies():
    
    all_taxonomies = taxonomies()
    return render_template('admin/taxonomias/taxonomias.html',all_taxonomies=all_taxonomies)

@app.route('/dashboard/taxonomias/<slug>')
def admin_edit_taxonomies(slug):
    taxonomy_title = get_taxonomy_title(slug)
    taxonomies = edit_taxonomie(slug)  # Call your function with the provided slug
    return render_template('admin/taxonomias/edit_taxonomia.html', taxonomies=taxonomies,taxonomy_title=taxonomy_title)

@app.route('/dashboard/taxonomias/relacoes')
def admin_taxonomies_rel():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    relations = taxonomies_relations()
    paginated_relations = list(islice(relations, (page - 1) * per_page, page * per_page))
    
    # Calculate pagination variables
    total_results = len(relations)
    total_pages = math.ceil(total_results / per_page)
    pagination = {
        'page': page,
        'per_page': per_page,
        'total_results': total_results,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1 if page > 1 else None,
        'next_num': page + 1 if page < total_pages else None,
        'iter_pages': range(1, total_pages + 1)
    }
    
    return render_template('admin/taxonomias/relacoes.html', relations=paginated_relations, pagination=pagination)

#######----------------####
@app.route('/dashboard/utilizadores')
def admin_users():
    all_users = get_all_users()
    return render_template('admin/utilizadores/utilizadores.html',all_users=all_users)












if __name__ == "__main__":
    app.run(debug=True)
