install:
	@pip install -r requirements.txt && pip install --upgrade pip

stop:
	@/bin/sh Docker/clear_docker_data.sh

start:
	@docker-compose -f Docker/docker-compose.yml up

test:
	@pytest src/tests/

