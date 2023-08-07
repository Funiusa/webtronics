# Makefile
D = docker
DC = docker-compose
DC_RUN = docker-compose run --rm
PORT = ${API_PORT}

api_add: # установить зависимости
	$(DC_RUN) -w /app/poetry api poetry add black $(ARGS)

bot_add: # установить зависимости
	$(DC_RUN) -w /app/poetry bot poetry add black $(ARGS)
up:
	$(DC) up

run_api:
	$(DC_RUN) -p 8088:8088 api $(ARGS)

re_api: clean build run_api

prune:
	$(D) system prune -a && $(D) volume prune -a && $(D) builder prune -f

test:
	$(DC_RUN) api pytest --verbosity 3

upd:
	$(DC_RUN) -d up $(ARGS)

build:
	$(DC) build

clean:
	$(DC) down;

info:
	docker system df

fclean: clean prune info
