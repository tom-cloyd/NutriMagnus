.PHONY: devserver build clean

devserver: build
	./dist/nutrimagnus

build:
	.venv/bin/pyinstaller --onefile --name nutrimagnus numa.py

clean:
	rm -rf build/ dist/ nutrimagnus.spec
