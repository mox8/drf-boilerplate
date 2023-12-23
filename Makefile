SHELL := /bin/bash

f = docker-compose.yml
db_host=localhost
db_port=5432

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null

build:
	docker-compose -f $(f) build

up:
	docker-compose -f $(f) up -d

down:
	docker-compose -f $(f) down

drm:
	docker-compose -f $(f) down -v --remove-orphans

lg:
	docker-compose -f $(f) logs -f

bup: build up

bupl: build up lg

dbup: down bup

dbupl: down bupl

ps:
	docker ps -a

sh:
	docker-compose -f $(f) exec app python manage.py shell

mkm:
	docker-compose -f $(f) exec app python manage.py makemigrations

mg:
	docker-compose -f $(f) exec app python manage.py migrate

migid:
	docker-compose -f $(f) exec app python manage.py migrate apps $(migid)

shmg:
	docker-compose -f $(f) exec app python manage.py showmigrations

admin:
	docker-compose -f $(f) exec app python manage.py createsuperuser --username admin

django-dump:
	docker-compose -f $(f) exec app python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.permission --indent 2 > services/backend/service/dump.json

django-load:
	docker-compose -f $(f) exec app python manage.py loaddata dump.json

pg-dump:
	./services/backend/scripts/db_dump.sh -h $(db_host) -p $(db_port) -n $(db_name) -u $(db_user) -P $(db_pass) -d $(export_dir)

pg-load:
	./services/backend/scripts/db_load.sh -h $(db_host) -p $(db_port) -n $(db_name) -u $(db_user) -P $(db_pass) -f $(dump_filename)

psql:
	./services/backend/scripts/db_connect.sh -h $(db_host) -p $(db_port) -n $(db_name) -u $(db_user) -P $(db_pass)
