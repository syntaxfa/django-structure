.PHONY: lint test

ROOT=$(realpath $(dir $(lastword $(MAKEFILE_LIST))))

lint:
	pylint $(ROOT)

test:
	python manage.py test

docker-test-up:
	docker compose -f $(ROOT)/compose-development.yml up -d

docker-test-down:
	docker compose -f $(ROOT)/compose-development.yml down
