CI_PROJECT_NAME ?= $(shell python3 setup.py --name)

all:
	@echo "make devenv	- Configure dev environment"
	@echo "make build	- Build Docker image"
	@echo "make clean	- Remove files created by distutils & dev modules"
	@echo "make test	- Run tests"
	@exit 0


devenv:
	rm -rf env
	virtualenv env -p python3
	env/bin/pip install -Ue '.[develop]'

clean:
	rm -fr *.egg-info .tox dist

sdist: clean
	env/bin/python setup.py sdist

build: clean sdist
	docker build -t storefront:latest .

test:
	env/bin/tox