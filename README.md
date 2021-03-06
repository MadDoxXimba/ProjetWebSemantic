# WEB SERVER FOR WEB SEMANTIC

- @author: Jonathan YUE CHUN
- @author: Quentin LEVAVASSEUR
- @author: Valentin Bouchevreau

# APACHE FUSEKI Sparql Server refer to this repository: https://github.com/MadDoxXimba/apache_fuseki_heroku 

## Pushing to branch master will deploy automatically to the web server below

    https://ontologie.herokuapp.com/

## Local debugging
    
Place in root directory (CMD or Powershell or Bash) - application must already be deployed, if not please follow this tutorial: https://devcenter.heroku.com/articles/git (if app is already deployed: skip to step 4)

    1) install heroku cli
    2) create heroku account
    3) heroku login (with your credentials)
    4) install virtualenv and virtualenvwrapper (see next section for guidelines) - if you don't want to use virtualenv, this step is not necessary! skip to step 6
    5) create virtualenv for your application with python 3.6.2 (see next section for guidelines)
    5) workon (yourvirtualenv_name)
    6) cd in clone directory
    7) pip install -r requirements.txt 
    8) heroku local
    
### TO EXIT the virtualenv
Place in root directory (Powershell or Bash)

    deactivate

### INSTALLATION of virtualenv on linux

refer to : https://virtualenv.pypa.io/en/stable/ and http://www.configserverfirewall.com/ubuntu-linux/create-python-virtualenv-ubuntu/

    1) install virtualenv and virtualenvwrapper
    2) clone project in your file system
    3) cd in project root folder (where requirements.txt are found)
    4) 1st time only: mkvirtualenv websemantic --python=/usr/bin/python3.6.2   (can be another path)
    5) pip install -r requirements.txt

Configuration:

#### Python Virtualenv Settings in ~/.bashrc (reload after edit source ~/.bashrc)

    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.6.2
    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/python_projects
    source /usr/local/bin/virtualenvwrapper.sh
    
### ENVIRONEMENT Variables

in $WORKON_HOME
    
    Define all environement variables in your virtualenv postactivate script and postdeactivate
    
        1) set environement variable in postactivate (ex: export JAVA_HOME=/path/to/java/home)
        2) unset environement variable define in postactivate by declaring the following in postdeactivate : unset JAVA_HOME
    

## Tutorials

    http://www.postgresqltutorial.com/postgresql-python


By students of Polytech Nantes
