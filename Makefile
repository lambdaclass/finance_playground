BUILD_DIR = build

.PHONY: default evaluating_gambles 
default: index evaluating_gambles 

dev: default
	python -m http.server

evaluating_gambles:
	mkdir -p build/evaluating_gambles/img
	mkdir -p build/evaluating_gambles/css
	-cp -R ./evaluating_gambles/img/* $(BUILD_DIR)/evaluating_gambles/img/
	-cp -R ./evaluating_gambles/css/* $(BUILD_DIR)/evaluating_gambles/css/
	pandoc ./evaluating_gambles/README.md --template ./evaluating_gambles/template.tmpl -t html5 --mathjax -o $(BUILD_DIR)/evaluating_gambles/index.html --metadata title="Emergence of Cooperation"

index:
	mkdir -p $(BUILD_DIR)
	pandoc README.md --template ./template.tmpl -t html5 -o $(BUILD_DIR)/index.html --metadata title="LambdaClass Data Études"