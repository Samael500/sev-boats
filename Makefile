test:
	. venv/bin/activate; nosetests --color --nologcapture sev-boats

ci_test:
	nosetests --color --nologcapture --with-coverage sev-boats
	make pep8
	make pyflakes

pep8:
	pep8 --max-line-length=119 --show-source sev-boats/

pyflakes:
	pylama -l pyflakes sev-boats/