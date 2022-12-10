all: run

run:
	python -m main

configure:
	./env/Scripts/Activate
	pip install -r requirements.txt

clean:
	$(RM) *.zip *.rar
