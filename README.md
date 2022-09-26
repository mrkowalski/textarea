# textarea

# How to start, locally

* `git clone git@github.com:mrkowalski/textarea.git`
* `cd textarea`
* set up python env somehow. I assume https://github.com/pyenv/pyenv-installer: `curl https://pyenv.run | bash`
* pyenv install 3.10.6
* pyenv virtualenv 3.10.6 textarea
* pyenv activate textearea
* pip install -r requirements.txt
* gunicorn --bind :<TCP_PORT> main:application
