.PHONY: lint test

ROOT=$(realpath $(dir $(lastword $(MAKEFILE_LIST))))

lint:
	pylint .

test:
	python manage.py test

docker-test-up:
	docker compose -f $(ROOT)/docker-compose-development.yml up -d

docker-test-down:
	docker compose -f $(ROOT)/docker-compose-development.yml down
