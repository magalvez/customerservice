To use pipenv follow this steps:

1) pip install pipenv
2) pipenv shell
3) pipenv install

Pipenv is going to look automatically the Pipfile and install the dependencies

Note if you want to analyze your dependencies you can run:

* pipenv graph

Yo will something like this:

Flask==1.1.2

- click [required: >=5.1, installed: 7.1.2]
- itsdangerous [required: >=0.24, installed: 1.1.0]
- Jinja2 [required: >=2.10.1, installed: 2.11.3]
    - MarkupSafe [required: >=0.23, installed: 1.1.1]
- Werkzeug [required: >=0.15, installed: 1.0.1]

Pipenv will generate a Pipfile.lock file to manages the following:

* The Pipfile.lock file enables deterministic builds by specifying the exact requirements for reproducing an
  environment. It contains exact versions for packages and hashes to support more secure verification