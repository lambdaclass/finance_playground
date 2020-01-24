BUILD_DIR = build

.PHONY: default emergence_of_cooperation html
default: index emergence_of_cooperation html

dev: default
	python -m http.server

emergence_of_cooperation:
	mkdir -p build/emergence_of_cooperation/img
	mkdir -p build/emergence_of_cooperation/css
	-cp -R ./emergence_of_cooperation/img/* $(BUILD_DIR)/emergence_of_cooperation/img/
	-cp -R ./emergence_of_cooperation/css/* $(BUILD_DIR)/emergence_of_cooperation/css/
	pandoc ./emergence_of_cooperation/README.md --template ./emergence_of_cooperation/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/emergence_of_cooperation/index.html --metadata title="Emergence of Cooperation"

index:
	mkdir -p $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)/css

	-cp -R ./css/* $(BUILD_DIR)/css/
	pandoc README.md --template ./template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/index.html --metadata title="LambdaClass Finance Playground"

html:
	mkdir -p $(BUILD_DIR)/rgbm_animation
	-cp -R ./html/rgbm_animation/* $(BUILD_DIR)/rgbm_animation
	cd $(BUILD_DIR)/rgbm_animation && npm install && npm run build
	rm -rf $(BUILD_DIR)/rgbm_animation/node_modules/