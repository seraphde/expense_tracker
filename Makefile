install:
	pip install -r requirements.txt

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

run:
	python manage.py runserver

shell:
	python manage.py shell_plushtt§