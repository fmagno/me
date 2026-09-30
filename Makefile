.PHONY: all pdf site serve clean

all:            ## build dist/cv.pdf and dist/index.html
	./build.py

pdf:            ## CV only
	./build.py pdf

site:           ## landing page only
	./build.py site

serve: all      ## preview at http://localhost:8765
	python3 -m http.server 8765 -d dist

clean:
	rm -rf dist
