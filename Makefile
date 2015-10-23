all: init plots analysis

init:
	@mkdir -p build

analysis:
	@python -m analysis analysis >> stdout.log 2>> stderr.log

plots:
	@python -m plots plots >> stdout.log 2>> stderr.log

clean:
	@rm -rf build
	@rm stdout.log
	@rm stderr.log

lint:
	@pylint analysis
	@pylint plots

.PHONY: build analysis plots
