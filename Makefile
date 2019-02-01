.PHONY: init env testdata test scrape bench

init:
	pipenv install

env:
	pipenv shell

testdata:
	pipenv run python backtester/test/create_test_data.py

test:
	pipenv run python -m unittest discover -s backtester/test

scrape:
	pipenv run python -m data_scraper -t $$SYM

bench:
	pipenv run python backtester/test/run_benchmark.py
