MANAGE_SCRIPT	:= manage.py

run-dev:
	@sudo docker-compose up -d

perms:
	@sudo chown -R ${USER}:${USER} .
