all: init docs plots

init:
	@mkdir -p build

docs:
	@pdoc --html --html-dir ./docs --overwrite ./plots

plots:
	@python -m plots plots >> stdout.log 2>> stderr.log

clean:
	@rm -rf docs
	@rm -rf build
	@rm stdout.log
	@rm stderr.log

lint:
	@pylint plots

.PHONY: docs build plots
