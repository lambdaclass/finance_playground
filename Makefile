BUILD_DIR = build

.PHONY: default diversification_dalio_holy_grail html
default: index diversification_dalio_holy_grail html

dev: default
	python -m http.server

diversification_dalio_holy_grail:
	#mkdir -p build/diversification_dalio_holy_grail/img
	mkdir -p build/diversification_dalio_holy_grail/css
	#-cp -R ./diversification_dalio_holy_grail/img/* $(BUILD_DIR)/diversification_dalio_holy_grail/img/
	-cp -R ./diversification_dalio_holy_grail/css/* $(BUILD_DIR)/diversification_dalio_holy_grail/css/
	pandoc ./diversification_dalio_holy_grail/README.md --template ./diversification_dalio_holy_grail/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/diversification_dalio_holy_grail/index.html --metadata title="Emergence of Cooperation"

index:
	mkdir -p $(BUILD_DIR)
	pandoc README.md --template ./template.tmpl -t html5 -o $(BUILD_DIR)/index.html --metadata title="LambdaClass finance playground"

html:
