BUILD_DIR = build

.PHONY: default soy_price_prediction html
default: index soy_price_prediction html

dev: default
	python -m http.server

soy_price_prediction:
	mkdir -p build/soy_price_prediction/img
	mkdir -p build/soy_price_prediction/css
	-cp -R ./soy_price_prediction/img/* $(BUILD_DIR)/soy_price_prediction/img/
	-cp -R ./soy_price_prediction/css/* $(BUILD_DIR)/soy_price_prediction/css/
	pandoc ./soy_price_prediction/README.md --template ./soy_price_prediction/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/soy_price_prediction/index.html --metadata title="Soy Price Prediction"

index:
	mkdir -p $(BUILD_DIR)
	pandoc README.md --template ./template.tmpl -t html5 -o $(BUILD_DIR)/index.html --metadata title="LambdaClass Finance Playground"

html: