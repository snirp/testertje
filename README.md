##Flatfreeze explanation and use case

Flatfreeze is a reference implementation of a static site generator ([Frozen-Flask]()) using Github Pages. [Github Pages]() only supports static sites, which are suited for anything that falls short of a web application (company pages, blogs, personal webpages).

Github Pages actually has a static site generator called Jekyll built in. Jekyll unfortunately gets templating wrong -no support for template inheritance- and is very closely tied to blogging. That means your are forced to use dates in your filenames and it leaves the bad taste of Wordpress blogs with tags and monthly archives.

When building the page for my company [Snirp](), I came across a better alternative: [Flask]() together with [Flask-Flatpages](). Some of the advatages of the approach include:

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

We refer to main.ccs file using a template tag. When Flask renders the template, this tag is replaced with the correct link. Let's make sure we have `/static/css/main.ccs`

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

We now have a Flask app running locally on the development server. It is dead easy to freeze this to the gh-pages folder:

```
venv$ python freeze.py
venv$ cd gh-pages
venv$ ls
index.html   static
```

You can open the index.html file in your browser. Test to see that it look just the same as before. Lets push the result to Github for the whole world to see. Still in the gh-pages folder do:


```
venv$ git add .
venv$ git commit -m "first frozen page"
venv$ git push
```

Check out the result on [username].github.io/[reponame]
