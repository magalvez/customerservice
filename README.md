# customerservice

## Prepare your environment

    ## 1) mkdir Playvox (check if was already created)
    ## 2) cd Playvox
    ## 3) git clone https://github.com/magalvez/customerservice.git
    ## 4) docker-compose up -d

# Service URL
http://localhost:8400/

## Testing via postmant
To test it with postman use the following collection:
https://www.getpostman.com/collections/e1daefda0d281339afeb

This is how you should upload the workflow.json
<img src="https://firebasestorage.googleapis.com/v0/b/tennis-rank-prod.appspot.com/o/static%2FScreen%20Shot%202021-05-07%20at%209.00.12%20AM.png?alt=media&token=8dfda06b-eec0-4b35-bcdf-8a8f54284a99"></img>


---------------------------------------------

To use without dokcer pipenv follow this steps:

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
  * The Pipfile.lock file enables deterministic builds by specifying the exact 
    requirements for reproducing an environment. It contains exact versions for 
    packages and hashes to support more secure verification