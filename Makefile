python := python manage.py

# make run => python manage.py runserver
run:
	$(python) runserver

# make migrate => python manage.py makemigrations && python manage.py migrate
migrate:
	$(python) makemigrations
	$(python) migrate

# make superuser => python manage.py createsuperuser
superuser:
	$(python) createsuperuser

app := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

# make app <app_name> => python manage.py startapp <app_name>
app:
	$(python) startapp $(app)

# make anything => python manage.py anything
%:
	$(python) $@