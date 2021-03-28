env:
	@python3 -m venv env
install:
	@pip install -r requirements.txt
serve:
	@export FLASK_APP=wsgi.py FLASK_ENV=development && flask run
freeze:
	@pip freeze | grep -v "pkg-resources" > requirements.txt