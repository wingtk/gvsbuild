#
# hacking about with gvsbuild. 
# this is a palceholder for various command line varieties.
# so far only the .venv build has worked.
#
#

# change on command line with `make PROJECT=gtk4` for example
PROJECT?=gtk3
# release|debug
CONFIG=release

# must be fully qualified else things break
# change these paths to suit your own conditions/installation
BUILD_DIR=r:/src/gtk/gvs-$(CONFIG)
MSYS_DIR=r:/apps/msys64

.PHONY: build rebuild install gvs help

all: help

help:
	@echo "make gvs: using gvsbuild."
	@echo "make install: install gvsbuild."
	@echo "make build: using Python."
	@echo "make rebuild: using Python. do it all from scratch. achtung baby."
	@echo "------------------------------"
	@echo "Override defaults with 'make PROJECT=librsvg' for example"
	@echo "PROJECT:$(PROJECT) CONFIG:$(CONFIG)"
	@echo "BUILD_DIR:$(BUILD_DIR) MSYS_DIR:$(MSYS_DIR)"

build:
	@echo "Project is $(PROJECT)"
	-rm $(BUILD_DIR)/logs/*.txt
	python starter.py build --ninja-opts -j=2 --build-dir $(BUILD_DIR) --log-single --capture-out --msys-dir  $(MSYS_DIR) --configuration $(CONFIG) $(PROJECT)

rebuild: 
	@echo "Project is $(PROJECT)"
	-rm $(BUILD_DIR)/logs/*.txt
	# python gvsbuild/main.py build --from-scratch --ninja-opts -j=2 --build-dir $(BUILD_DIR) --msys-dir  r:\apps\msys64 --configuration debug $(PROJECT)
	python starter.py build --from-scratch --ninja-opts -j=2 --build-dir $(BUILD_DIR) --msys-dir $(MSYS_DIR) --log-single --capture-out --configuration $(CONFIG) $(PROJECT)

# install gvsbuild into the local Python cache
install:
	pip install .

gvs:	
	gvsbuild build --from-scratch --ninja-opts -j=2 --build-dir $(BUILD_DIR) --msys-dir $(MSYS_DIR) --log-single --capture-out --configuration release $(PROJECT)

#
# Fixed with modified libpng.py project	
# hack:
#	cp checksym.awk .\build\build\x64\debug\libpng\_gvsbuild-cmake\scripts
