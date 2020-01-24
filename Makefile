BUILD_DIR = build

.PHONY: default troubled_markets_and_volatility index
default: troubled_markets_and_volatility index

dev: default
	python -m http.server

troubled_markets_and_volatility:
	mkdir -p $(BUILD_DIR)/troubled_markets_and_volatility/img
	mkdir -p $(BUILD_DIR)/troubled_markets_and_volatility/css
	-cp -R ./troubled_markets_and_volatility/img/* $(BUILD_DIR)/troubled_markets_and_volatility/img/
	-cp -R ./troubled_markets_and_volatility/css/* $(BUILD_DIR)/troubled_markets_and_volatility/css/
	pandoc ./troubled_markets_and_volatility/README.md --template ./troubled_markets_and_volatility/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/troubled_markets_and_volatility/index.html --metadata title="Troubled Markets and Volatility"

index:
	mkdir -p $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)/css

	-cp -R ./css/* $(BUILD_DIR)/css/
	pandoc README.md --template ./template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/index.html --metadata title="LambdaClass Finance Playground"

html:
	cd $(BUILD_DIR)/rgbm_animation && npm install && npm run build
	rm -rf $(BUILD_DIR)/rgbm_animation/node_modules/