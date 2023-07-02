#
# hacking about with gvsbuild. 
# this is a palceholder for various command line varieties.
# so far only the .venv build has worked.
#
#

#
PROJECT=gtk3

# must be fully qualified else things break
# chnage these paths to suit your own conditions/installation
BUILD_DIR=r:/src/gtk/gvs-outputs
MSYS_DIR=r:/apps/msys64
CONFIG=release

.PHONY: build rebuild install help

all: help

help:
	@echo "override default $(PROJECT) with make PROJECT=gtk3 for example"
	@echo "make build: build the nominated project. default:$(PROJECT)"
	@echo "make install: build and install gvsbuild. default:$(PROJECT)"
	@echo "make rebuild: do it all from scratch. achtung baby."

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
	
install-ps:
	# powershell
	python -m pip install --user pipx
	python -m pipx ensurepath
	pipx install gvsbuild

build-ps:
	# make cannot do this for you. these are the steps ...
	python -m venv .venv
	.\.venv\Scripts\activate.ps1
	pip install .
	gvsbuild build --from-scratch --ninja-opts -j=2 --build-dir $(BUILD_DIR) --msys-dir $(MSYS_DIR) --log-single --capture-out --configuration $(CONFIG) $(PROJECT)

#
# Fixed with modified libpng.py project	
# hack:
#	cp checksym.awk .\build\build\x64\debug\libpng\_gvsbuild-cmake\scripts
