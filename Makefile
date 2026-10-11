.PHONY: run compile test test-services docker-build docker-test

run:
	python app.py

compile:
	python -m compileall -q app.py services.py tests

test:
	python -m pytest -q

test-services:
	python -m pytest -q tests/test_services.py

docker-build:
	docker build --target runtime -t aceest-fitness:latest .

docker-test:
	docker build --target test -t aceest-fitness-test:latest .
