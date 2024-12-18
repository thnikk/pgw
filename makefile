install:
	mkdir -p venv
	python -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install pyinstaller
	venv/bin/pyinstaller pgw.spec
	cp dist/pgw ~/.local/bin/

clean:
	rm -rf venv
	rm -rf dist
	rm -rf build
