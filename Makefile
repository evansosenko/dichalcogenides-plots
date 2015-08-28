all: plots analysis

analysis:
	@python analysis >> stdout.log 2>> stderr.log

plots:
	@python plots >> stdout.log 2>> stderr.log

clean:
	@rm -rf build
	@rm stdout.log
	@rm stderr.log

.PHONY: build analysis plots
