recreate:
	docker-compose down
	docker-compose up -d
migrate:
	python src/manage.py migrate
run:
	python src/manage.py runserver
test:
	python3 -m pytest src
celery:
	celery -A config worker --loglevel=INFO
