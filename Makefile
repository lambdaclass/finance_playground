HTML_DIR = html
NOTEBOOKS_DIR = notebooks

.PHONY: html

html:
	-mkdir -p $(HTML_DIR)
	-shopt -s globstar
	cp -R $(NOTEBOOKS_DIR)/* $(HTML_DIR)
	-jupyter nbconvert $(HTML_DIR)/*.ipynb
	-jupyter nbconvert $(HTML_DIR)/**/*.ipynb
	-rm $(HTML_DIR)/*.ipynb
	-rm $(HTML_DIR)/**/*.ipynb
	cd html/rgbm_animation
	npm install
	npm run build
