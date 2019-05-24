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
	tree $(HTML_DIR)/ -H '.' -C --noreport --charset utf-8 > $(HTML_DIR)/index.html
