PROJECT_NAME ?= $(shell python3 setup.py --name)
PROJECT_VERSION ?= $(shell python3 setup.py --version)

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
	docker build \
	  -t janeturueva/${PROJECT_NAME}:latest \
	  -t janeturueva/${PROJECT_NAME}:${PROJECT_VERSION} .

upload: build
	docker push janeturueva/${PROJECT_NAME}:latest
	docker push janeturueva/${PROJECT_NAME}:${PROJECT_VERSION}

test:
	env/bin/tox