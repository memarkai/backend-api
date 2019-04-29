MANAGE_SCRIPT	:= manage.py

all: build run-dev

build:
	@pip3 install -r requirements.txt

run-dev:
	@sudo docker-compose up -d
	@python3 -m envdir env/dev/ python3 $(MANAGE_SCRIPT) runserver 127.0.0.1:8000
