all: init docs plots analysis

init:
	@mkdir -p build

docs:
	@pdoc --html --html-dir ./docs --overwrite ./analysis
	@pdoc --html --html-dir ./docs --overwrite ./plots

analysis:
	@python -m analysis analysis >> stdout.log 2>> stderr.log

plots:
	@python -m plots plots >> stdout.log 2>> stderr.log

clean:
	@rm -rf docs
	@rm -rf build
	@rm stdout.log
	@rm stderr.log

lint:
	@pylint analysis
	@pylint plots

.PHONY: docs build analysis plots
