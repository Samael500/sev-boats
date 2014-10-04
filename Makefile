test:
	. venv/bin/activate; nosetests --color --nologcapture

ci_test:
	nosetests --color --nologcapture
	make pep8
	make pyflakes

pep8:
	pep8 --exclude=venv/* --max-line-length=119 --show-source */

pyflakes:
	pylama --skip=venv/* -l pyflakes