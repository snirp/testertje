from flask import Flask, render_template

# initialization
app = Flask(__name__)

# configuration
app.config['FREEZER_DESTINATION'] = 'gh-pages'
app.config['FREEZER_DESTINATION_IGNORE'] = ['.git*', 'CNAME', '.gitignore', 'readme.md']
app.config['FREEZER_RELATIVE_URLS'] = True

# controllers
@app.route("/")
def index():
    return render_template('index.html')

# launch
if __name__ == "__main__":
    app.run(debug=True)