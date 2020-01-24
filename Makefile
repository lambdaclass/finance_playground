BUILD_DIR = build

.PHONY: default intro_finance index
default:  intro_finance index

dev: default
	python -m http.server

intro_finance:
	mkdir -p build/intro_finance/img
	mkdir -p build/intro_finance/css
	-cp -R ./intro_finance/img/* $(BUILD_DIR)/intro_finance/img/
	-cp -R ./intro_finance/css/* $(BUILD_DIR)/intro_finance/css/
	pandoc ./intro_finance/README.md --template ./intro_finance/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/intro_finance/Intro_Finance.html --metadata title="Intro Finance"
	pandoc README.md --template ./template.tmpl -t html5 -o $(BUILD_DIR)/index.html --metadata title="LambdaClass Finance Playground"

index:
	mkdir -p $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)/css

	-cp -R ./css/* $(BUILD_DIR)/css/
	pandoc README.md --template ./template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/index.html --metadata title="LambdaClass Finance Playground"
html:
	cd html/rgbm_animation && npm install && npm run build
	rm -rf html/rgbm_animation/node_modules/
