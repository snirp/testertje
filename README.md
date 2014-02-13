##Flatfreeze explanation and use case

Flatfreeze is a reference implementation of a static site generator ([Frozen-Flask]()) using Github Pages. [Github Pages]() only supports static sites, which are suited for anything that falls short of a web application (company pages, blogs, personal webpages).

Github Pages actually has a static site generator called Jekyll built in. Jekyll unfortunately gets templating wrong -no support for template inheritance- and is very closely tied to blogging. That means your are forced to use dates in your filenames and it leaves the bad taste of Wordpress blogs with tags and monthly archives.

When building the page for my company [Snirp](http://snirp.nl), I came across a better alternative: [Flask]() together with [Flask-Flatpages](). Some of the advatages of the approach include:

* Proper templating with template inheritance;
* Free hosting on Github Pages, with optional use of a custom domain name;
* Static pages are fast and resilient;
* Write your articles in eye-pleasing Markdown;
* Versioning and updating through git (no messing around with ftp). 

Freezing to static pages is very straighforward. Fork this repository or follow the instructions below to set up a reference project and get going.


##Setting up the repository for Github Pages

This paragraph is *not* specific to Flatfreeze and I recommend you to follow these instructions when setting up Github Pages for use with other frameworks as well.


###step 0: The big picture


We will be using two braches within our repository. The **master** branch keeps track of the program code *except* the static pages. The **gh-pages** branch contains only the frozen static pages for publishing on Github Pages.

We want to organize our work in a project folder (generator-app) and a subfolder (gh-pages) that holds the static files. Our flask app lives in the project folder and it will 'freeze' static files to the subfolder.

```
/generator-app/            <-> master branch
/generator-app/gh-pages/   <-> gh-pages branch
```

This works nicely with Github: it requires the frozen files to be in a separate branch named "gh-pages". We can track everything else in the "master" branch.


###step 1: Create and clone an empty repository

We can start by creating a new repository on [github.com](https://github.com/new). Give it any name you wish; I chose "flatfreeze". We clone the repository into a new folder that corresponds with the /generator-app/ folder of step 0 and we make the subfolder "gh-pages".

```
$ git clone https://github.com/snirp/flatfreeze.git
Cloning into 'flatfreeze'...
$ cd flatfreeze
$ mkdir gh-pages
```


###step 2: Exclude the gh-pages folder

As we said earlier, we want to track all the code *except* the frozen gh-pages in the master branch. Let's exclude the gh-pages folder by adding a .gitignore file.

```
$ echo "gh-pages" > .gitignore
$ git add .gitignore
$ git commit -a -m "First commit on master"
$ git push origin master
To https://github.com/snirp/flatfreeze.git
 * [new branch]      master -> master
```

Note: it is not stricly necassary to exclude this folder from the master-branch, but it simply seems a lot cleaner.

###step 3: Set up the gh-pages branch

As recommended in the [documentation](https://help.github.com/articles/creating-project-pages-manually) we create the gh-pages branch as an orphaned branch. The following is said about orphan branches:

>The first commit made on this new branch will have no parents and it will be the root of a new history totally disconnected from all the other branches and commits.

We will again clone the repository, now into the gh-pages folder, and create the gh-pages branch there. Any old files are deleted by `git rm -rf .`.

```
$ cd gh-pages
$ git clone https://github.com/snirp/flatfreeze.git . #mind the dot there
$ git checkout --orphan gh-pages
Switched to a new branch 'gh-pages'
$ git rm -rf .
rm '.gitignore'
```

###step 4: Put it to the test

Lets create and push a simple HTML file to gh-pages. While still operating in the gh-pages branch, do the following:

```
$ echo "hello world" > index.html
$ git add index.html
$ git commit -a -m "First commit on gh-pages"
To https://github.com/snirp/flat-flask.git
 * [new branch]      gh-pages -> gh-pages
$ git push origin gh-pages
```

Behind the scenes Github works its magic. If a branch named "gh-pages" is present, the contents are made available on
http://{username}.github.io/{reponame}/. Our little "Hello world" is on [snirp.github.io/flat-flask/](snirp.github.io/flatfreeze/).

The project folder should be like this:

```
/flatfreeze/
/flatfreeze/.git  #linked to master
/flatfreeze/.gitignore
/flatfreeze/gh-pages/
/flatfreeze/gh-pages/.git  #linked to gh-pages
/flatfreeze/gh-pages/index.html
```
And the Github repository resembles:

```
master branch: .gitignore
===========================
gh-pages branch: index.html
```

###step 5: Clean up

Two branches still exist in the cloned repository in the gh-pages folder. Let's delete the master branch, since it is of not much use. Finally we check that only the gh-pages branch remains.


```
$ git branch
* gh-pages
  master
$ git branch -d master
warning: deleting ...
$ git branch
* gh-pages
```


##Set up the project

Flask is a Python framework, so let's set up a virtualenvironment and the dependencies first. If you are not using virtualenvironments for your Python projects, you really should. Inside the project/root folder do:

```
$ virtualenv venv --distribute
Installing pip........done
$ source venv/bin/activate
(venv)$ pip install frozen-flask
(venv)$ pip install flask-flatpages
(venv)$ pip freeze > requirements.txt
```

These commands install everything we need. To recap:

* Flask-flatpages takes markdown files, renders them to HTML and parses the metadata of the first lines of the file.
* Frozen-flask freezes a dynamic Flask application into a set of static files in a different folder.

Flask is a minimalistic webframework, which needs only a single python file `app.py` and two folders named by convention as `/templates` and `/static`. In case you are not familiar with Flask, the [quickstart guide](http://flask.pocoo.org/docs/quickstart/) will cover everything you need here.

```
/flatfreeze/.gitignore
/flatfreeze/app.py
/flatfreeze/freeze.py
/flatfreeze/templates/base.html
/flatfreeze/templates/index.html
/flatfreeze/static/css/main.css
```

We add some more lines to `.gitignore`

```
gh-pages
venv
.idea
*.pyc
*~
.DS_Store
.idea
```

We will need some settings for frozen-flask: first we need to tell what folder it can put the frozen files into. 

* FREEZER_DESTINATION = 'gh-pages'

It will delete or override all files in that folder, unless we exclude them explicitly. Let's do that next. 

* FREEZER_DESTINATION_IGNORE = ['.git*', 'CNAME', '.gitignore', 'readme.md']

Finally we will be moving our folder to github, so we don't want to tie the URL's to our filesystem.

* FREEZER_RELATIVE_URLS = True

Other than that, we will use a default `app.py`:

```
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
```

That takes care of the basics. You can try running your application for the first time:

```
venv$ python app.py
* Running on http://127.0.0.1:5000/
```

Surf to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) and you will be greeted with an error. No panic, we did not define our templates yet.

Lets set up a minimal basic skeleton that all our pages can use. This is what template inheritance is about. `/templates/base.html`:

```
<!DOCTYPE html>
<html lang="en">
<head>
{% block head %}
  <title>{% if title %}{{title}}{% else %}Flatfreeze{% endif %}</title>
  <meta charset="utf-8">
  {% if description %}
    <meta name="description" content="{{description}}">
  {% else %}
    <meta name="description" content="Flatfreeze flattens & freezes in one go!">
  {% endif %}
{% endblock %}
</head>
<body>
  {% block content %}
  {% endblock %}
</body>
</html>
```

Our `/templates/index.html` extends from the 'base.html' template.


```
{% extends 'base.html' %}
{% block head %}
  {{ super() }}
  <link rel='stylesheet' href="{{ url_for('static', filename='css/main.css') }}">
{% endblock %}
{% block content %}
  <h1>flatfreeze</h1>
  <p>Flatten & freeze in one go!</p>
{% endblock %}
```

We refer to main.ccs file using a template tag. When Flask renders the template, this tag is replaced with the correct link. Let's make sure we have `/static/css/main.ccs`:

```
h1 {
  padding: 50px 0;
  font-size:2.5em;
  margin: 0 auto;
}
p {
  max-width: 700px;
  font-size:1.25em;
  margin: 0 auto;
}
```

Restart the development server to see our shiny page at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

```
venv$ python app.py
* Running on http://127.0.0.1:5000/
```


##Freeze and publish

We now have a Flask app running locally on the development server. Let's commit the current state and next freeze this to the gh-pages folder:

```
venv$ git add .
venv$ git commit -m "working Flask app"
venv$ git push origin master
venv$ python freeze.py
venv$ cd gh-pages
venv$ ls
index.html   static
```

You can open the index.html file in your browser. Test to see that it looks just as expected. Lets push the result to Github for the whole world to see. Still in the gh-pages folder do:


```
venv$ git add .
venv$ git commit -m "first frozen page"
venv$ git push origin gh-pages
```

Check out the result on [username].github.io/[reponame].

###additional files

We can set up a custom domain by adding a file named `CNAME` to the gh-pages folder with only the domain name:

```
flatfreeze.com
```

Now make some DNS changes and point the A record of your domain to `192.30.252.153` and `192.30.252.154`. Wait 24 hours for changes to take effect. Refer to the [Github documentation](https://help.github.com/articles/setting-up-a-custom-domain-with-pages) for more details.

Add a `readme.md` file to the same folder to document your repository:

```
##About the branch
This gh-pages branch was generated using [frozen-flask]
(http://pythonhosted.org/Frozen-Flask/) and is hosted 
through [Github Pages](http://pages.github.com/). 
See the end result at [flatfreeze.com](http://flatfreeze.com).
##See the code
The application code can be viewed by switching to the 
[master branch](https://github.com/snirp/flatfreeze/tree/master).
```

We did not yet add a `.gitignore` file to the gh-pages branch. Let's take care of that:

```
.idea
*.pyc
*~
.DS_Store
.idea
```

Remember that we already included these files in the ignore-list:

* FREEZER_DESTINATION_IGNORE = ['.git*', 'CNAME', '.gitignore', 'readme.md']

That means these will not be deleted the next time we freeze the application.

###Contact page, sitemap and 404

Most websites have some added complexity beyond the index.html page. In our case this will ammount to a contact.html page, a sitemap.xml and a 404 not found page. For each of these, we will add a template. Some new template tags are introduced, so if you not yet comfortable with Flask/Jinja2 templating, refer to the [documentation](http://jinja.pocoo.org/docs/templates/).

The `/templates/contact.html` is similar to our index.html.

```
{% extends 'base.html' %}
{% block head %}
  {{ super() }}
  <link rel='stylesheet' href="{{ url_for('static', filename='css/main.css') }}">
{% endblock %}
{% block content %}
  <h1>contact us</h1>
  <ul>
    <li>call us <a href="tel:0800-54321">0800-54321</a></li>
    <li>mail us <a href="mailto:i@flatfreeze.com">i@flatfreeze.com</a></li>
    <li>visit us: 101st Street, New York, NY</li>
   </ul>
   back to <a href="{{ url_for('index') }}">index</a>
{% endblock %}
```

Ok, we are not winning prizes for design or usability here, but it gets the point across. Likewise we should make a `/templates/404.html` with a friendly error page.

```
{% extends 'base.html' %}
{% block content %}
<h1>page not found</h1>
<p>We have sent out Sir Henry Morton Stanley to try and find the
page for you. In the mean time you should probably return to the
<a href="{{ url_for('index') }}">homepage</a>.</p>
{% endblock %}
```

The final template is the `/templates/sitemap.xml` page. This serves to give the search engines information what locations to index and when to do so.

```
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {% for s in sites %}
    <url>
        <loc>{{s[0]|safe}}</loc>
        <lastmod>{{s[1]}}</lastmod>
    </url>
    {% endfor %}
</urlset>
```

All we have now is some templates. We need to set up the routing to tie it all together. Change `app.py` so it resembles:

```
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
        ('',              '2014-02-13'),
        ('contact.html',  '2014-02-13'),
    ]
    sites = [(SITEMAP_DOMAIN + l[0], l[1]) for l in locations]
    return render_template('sitemap.xml', sites=sites)

# launch
if __name__ == "__main__":
    app.run(debug=True)
```

Frozen-Flask follows the routes we have set up for `/`, `contact.html`, `404.html` and `sitemap.xml` and generates the related pages. Here we use two different setups for the `404` response:

1. A Flask app uses the errorhandler. This is only for when we run the app locally.
2. Github Pages expects a `404.html` page to exist and will serve that. Setting up the routing here guarantees that this page will exist.

The controller function for the sitemap is slightly more complex. This will however scale up nicely to include more locations and also pages created by Flask-Flatpages when we get to that.

We can now commit and push the changes so far run the application to see whether everything works. 

```
venv$ git add .
venv$ git commit -m "added 404, sitemap and contact page"
venv$ git push origin master
venv$ python app.py
```

dsddsds