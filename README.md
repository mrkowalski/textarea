# textarea

# How to start, locally

* git clone it
* cd to the folder
* set up python env somehow. I assume pyenv
* pyenv install 3.10.6
* pyenv virtualenv 3.10.6 textarea
* pyenv activate textearea
* pip install -r requirements.txt
* gunicorn --bind :<TCP_PORT> main:application
