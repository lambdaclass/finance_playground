BUILD_DIR = build


.PHONY: default emergence_of_cooperation troubled_markets_and_volatility ergodicity_explorations evaluating_gambles diversification_dalio_holy_grail soy_price_prediction references intro_finance html
default: index emergence_of_cooperation troubled_markets_and_volatility ergodicity_explorations evaluating_gambles diversification_dalio_holy_grail soy_price_prediction references intro_finance html

dev: default
	python -m http.server


troubled_markets_and_volatility:
	mkdir -p $(BUILD_DIR)/troubled_markets_and_volatility/img
	mkdir -p $(BUILD_DIR)/troubled_markets_and_volatility/css
	-cp -R ./troubled_markets_and_volatility/img/* $(BUILD_DIR)/troubled_markets_and_volatility/img/
	-cp -R ./troubled_markets_and_volatility/css/* $(BUILD_DIR)/troubled_markets_and_volatility/css/
	pandoc ./troubled_markets_and_volatility/README.md --template ./troubled_markets_and_volatility/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/troubled_markets_and_volatility/index.html --metadata title="Troubled Markets and Volatility"

emergence_of_cooperation:
	mkdir -p $(BUILD_DIR)/emergence_of_cooperation/img
	mkdir -p $(BUILD_DIR)/emergence_of_cooperation/css
	-cp -R ./emergence_of_cooperation/img/* $(BUILD_DIR)/emergence_of_cooperation/img/
	-cp -R ./emergence_of_cooperation/css/* $(BUILD_DIR)/emergence_of_cooperation/css/
	pandoc ./emergence_of_cooperation/README.md --template ./emergence_of_cooperation/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/emergence_of_cooperation/index.html --metadata title="Emergence of Cooperation"

ergodicity_explorations:
	mkdir -p $(BUILD_DIR)/ergodicity_explorations/img
	mkdir -p $(BUILD_DIR)/ergodicity_explorations/css
	-cp -R ./ergodicity_explorations/img/* $(BUILD_DIR)/ergodicity_explorations/img/
	-cp -R ./ergodicity_explorations/css/* $(BUILD_DIR)/ergodicity_explorations/css/
	pandoc ./ergodicity_explorations/README.md --template ./ergodicity_explorations/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/ergodicity_explorations/index.html --metadata title="Ergodicity Explorations"

evaluating_gambles:
	mkdir -p $(BUILD_DIR)/evaluating_gambles/img
	mkdir -p $(BUILD_DIR)/evaluating_gambles/css
	-cp -R ./evaluating_gambles/img/* $(BUILD_DIR)/evaluating_gambles/img/
	-cp -R ./evaluating_gambles/css/* $(BUILD_DIR)/evaluating_gambles/css/
	pandoc ./evaluating_gambles/README.md --template ./evaluating_gambles/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/evaluating_gambles/index.html --metadata title="Evaluating Gambles"

diversification_dalio_holy_grail:
	mkdir -p $(BUILD_DIR)/diversification_dalio_holy_grail/img
	mkdir -p $(BUILD_DIR)/diversification_dalio_holy_grail/css
	-cp -R ./diversification_dalio_holy_grail/css/* $(BUILD_DIR)/diversification_dalio_holy_grail/css/
	-cp -R ./diversification_dalio_holy_grail/img/* $(BUILD_DIR)/diversification_dalio_holy_grail/img/
	pandoc ./diversification_dalio_holy_grail/README.md --template ./diversification_dalio_holy_grail/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/diversification_dalio_holy_grail/index.html --metadata title="The Holy Grail of Investing"

soy_price_prediction:
	mkdir -p $(BUILD_DIR)/soy_price_prediction/img
	mkdir -p $(BUILD_DIR)/soy_price_prediction/css
	-cp -R ./soy_price_prediction/img/* $(BUILD_DIR)/soy_price_prediction/img/
	-cp -R ./soy_price_prediction/css/* $(BUILD_DIR)/soy_price_prediction/css/
	pandoc ./soy_price_prediction/README.md --template ./soy_price_prediction/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/soy_price_prediction/index.html --metadata title="Soy Price Prediction"

intro_finance:
	mkdir -p $(BUILD_DIR)/intro_finance/img
	mkdir -p $(BUILD_DIR)/intro_finance/css
	-cp -R ./intro_finance/img/* $(BUILD_DIR)/intro_finance/img/
	-cp -R ./intro_finance/css/* $(BUILD_DIR)/intro_finance/css/
	pandoc ./intro_finance/README.md --template ./intro_finance/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/intro_finance/index.html --metadata title="Introduction to Finance"

references:
	mkdir -p $(BUILD_DIR)/references/css
	-cp -R ./references/css/* $(BUILD_DIR)/references/css/
	pandoc ./references/README.md --template ./references/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/references/index.html --metadata title="References"

index:
	mkdir -p $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)/css
	mkdir -p $(BUILD_DIR)/img
	-cp -R ./css/* $(BUILD_DIR)/css/
	-cp -R ./img/* $(BUILD_DIR)/img/
	pandoc README.md --template ./template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/index.html --metadata title="LambdaClass Finance Playground"

html:
	mkdir -p $(BUILD_DIR)/rgbm_animation
	-cp -R ./html/rgbm_animation/* $(BUILD_DIR)/rgbm_animation
	cd $(BUILD_DIR)/rgbm_animation && npm install && npm run build
	rm -rf $(BUILD_DIR)/rgbm_animation/node_modules/
