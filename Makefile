APP=portfolio
JS_FILES=media/js/src media/js/src

all: jenkins

include *.mk

dev:
	trap 'kill 0' EXIT; make runserver & make scss
.PHONY: dev
