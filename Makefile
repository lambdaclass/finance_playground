.PHONY: init env testdata test scrape aggregate backup bench

init:
	pipenv --three && pipenv install

env:
	pipenv shell

testdata:
	pipenv run python backtester/test/create_test_data.py

test:
	pipenv run python -m unittest discover -s backtester/test

scrape:
	pipenv run python -m data_scraper -t $(symbols) -s $(scraper)

aggregate:
	pipenv run python -m data_scraper -a

backup:
	pipenv run python -m data_scraper -b
	
bench:
	pipenv run python backtester/test/run_benchmark.py
