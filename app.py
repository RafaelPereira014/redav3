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

# Tools
@app.route('/tools')
def tools():
    return render_template('tools.html')

# My Account
@app.route('/myaccount')
def my_account():
    return render_template('my_account.html')

# Admin Page
@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == "__main__":
    app.run(debug=True)
