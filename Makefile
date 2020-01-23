BUILD_DIR = build

.PHONY: default troubled_markets_and_volatility html
default: index troubled_markets_and_volatility 

dev: default
	python -m http.server

troubled_markets_and_volatility:
	mkdir -p build/troubled_markets_and_volatility/img
	mkdir -p build/troubled_markets_and_volatility/css
	-cp -R ./troubled_markets_and_volatility/img/* $(BUILD_DIR)/troubled_markets_and_volatility/img/
	-cp -R ./troubled_markets_and_volatility/css/* $(BUILD_DIR)/troubled_markets_and_volatility/css/
	pandoc ./troubled_markets_and_volatility/README.md --template ./troubled_markets_and_volatility/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/troubled_markets_and_volatility/index.html --metadata title="Troubled Markets and Volatility"

index:
	mkdir -p $(BUILD_DIR)
	pandoc README.md --template ./template.tmpl -t html5 -o $(BUILD_DIR)/index.html --metadata title="LambdaClass Finance Playground"

html:
	cd html/rgbm_animation && npm install && npm run build
	rm -rf html/rgbm_animation/node_modules/