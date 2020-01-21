BUILD_DIR = build

.PHONY: default emergence_of_cooperation html
default: index emergence_of_cooperation 

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
	pandoc README.md --template ./template.tmpl -t html5 -o $(BUILD_DIR)/index.html --metadata title="LambdaClass finance playground"

html:
	cd html/rgbm_animation && npm install && npm run build
	rm -rf html/rgbm_animation/node_modules/