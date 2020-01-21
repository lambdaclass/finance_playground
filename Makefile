BUILD_DIR = build

.PHONY: default ergodicity_explorations html
default: index ergodicity_explorations 

dev: default
	python -m http.server

ergodicity_explorations:
	mkdir -p build/ergodicity_explorations/img
	mkdir -p build/ergodicity_explorations/css
	-cp -R ./ergodicity_explorations/img/* $(BUILD_DIR)/ergodicity_explorations/img/
	-cp -R ./ergodicity_explorations/css/* $(BUILD_DIR)/ergodicity_explorations/css/
	pandoc ./ergodicity_explorations/README.md --template ./ergodicity_explorations/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/ergodicity_explorations/index.html --metadata title="Ergodicity Explorations"


index:
	mkdir -p $(BUILD_DIR)
	pandoc README.md --template ./template.tmpl -t html5 -o $(BUILD_DIR)/index.html --metadata title="LambdaClass Finance Playground"

html:
	cd html/rgbm_animation && npm install && npm run build
	rm -rf html/rgbm_animation/node_modules/