from flask import Flask, render_template

# initialization
app = Flask(__name__)

# configuration
app.config['FREEZER_DESTINATION'] = 'gh-pages'
app.config['FREEZER_DESTINATION_IGNORE'] = ['.git*', 'CNAME', '.gitignore', 'readme.md']
app.config['FREEZER_RELATIVE_URLS'] = True

SITEMAP_DOMAIN = 'http://flatfreeze.com/'

# controllers
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/404.html')
def static_404():
    return render_template('404.html')

@app.route('/sitemap.xml')
def generate_sitemap():
    locations = [
        ('',                '2014-02-13'),
        ('contact.html',    '2014-02-13'),
    ]
    sites = [(SITEMAP_DOMAIN + l[0], l[1]) for l in locations]
    return render_template('sitemap.xml', sites=sites)

# launch
if __name__ == "__main__":
    app.run(debug=True)