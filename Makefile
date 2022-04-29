APP=portfolio
JS_FILES=media/js/src media/js/src
SYS_PYTHON=python3

all: jenkins cypress

include *.mk

integrationserver: $(PY_SENTINAL)
	$(MANAGE) integrationserver --noinput

cypress: $(JS_SENTINAL)
	npm run cypress:test

dev:
	trap 'kill 0' EXIT; make runserver & make scss
.PHONY: dev
