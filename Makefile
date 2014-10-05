test:
	. venv/bin/activate; nosetests --color --nologcapture sevboats/

ci_test:
	nosetests --with-coverage --cover-package=sevboats --color sevboats/
	make pep8
	make pyflakes

pep8:
	pep8 --max-line-length=119 --show-source sevboats/

pyflakes:
	pylama -l pyflakes sevboats/
 