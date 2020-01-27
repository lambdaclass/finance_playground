BUILD_DIR = build


.PHONY: default emergence_of_cooperation troubled_markets_and_volatility ergodicity_explorations html
default: index emergence_of_cooperation troubled_markets_and_volatility ergodicity_explorations html


dev: default
	python -m http.server


troubled_markets_and_volatility:
	mkdir -p $(BUILD_DIR)/troubled_markets_and_volatility/img
	mkdir -p $(BUILD_DIR)/troubled_markets_and_volatility/css
	-cp -R ./troubled_markets_and_volatility/img/* $(BUILD_DIR)/troubled_markets_and_volatility/img/
	-cp -R ./troubled_markets_and_volatility/css/* $(BUILD_DIR)/troubled_markets_and_volatility/css/
	pandoc ./troubled_markets_and_volatility/README.md --template ./troubled_markets_and_volatility/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/troubled_markets_and_volatility/index.html --metadata title="Troubled Markets and Volatility"

emergence_of_cooperation:
	mkdir -p build/emergence_of_cooperation/img
	mkdir -p build/emergence_of_cooperation/css
	-cp -R ./emergence_of_cooperation/img/* $(BUILD_DIR)/emergence_of_cooperation/img/
	-cp -R ./emergence_of_cooperation/css/* $(BUILD_DIR)/emergence_of_cooperation/css/
	pandoc ./emergence_of_cooperation/README.md --template ./emergence_of_cooperation/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/emergence_of_cooperation/index.html --metadata title="Emergence of Cooperation"


ergodicity_explorations:
	mkdir -p build/ergodicity_explorations/img
	mkdir -p build/ergodicity_explorations/css
	-cp -R ./ergodicity_explorations/img/* $(BUILD_DIR)/ergodicity_explorations/img/
	-cp -R ./ergodicity_explorations/css/* $(BUILD_DIR)/ergodicity_explorations/css/
	pandoc ./ergodicity_explorations/README.md --template ./ergodicity_explorations/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/ergodicity_explorations/index.html --metadata title="Ergodicity Explorations"

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
	

