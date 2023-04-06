# 2023-01-04 Manjot Randhawa

# delete the target of a rule if the rule fails and a command exits with non-zero exit status
.DELETE_ON_ERROR:
SHELL := /usr/bin/bash

#----------------
# global functions
error_logger   = $(error [ERROR] $1)
info_logger    = $(info [INFO] $1)
shell_variable = $(shell which $1)
garbage_collector = $(foreach shit, $1, $(shell rm -rf ${shit} ||:))
#----------------

#----------------
# simple expansion variables
VENV_NAME                  := venv-project
RECOMMENDED_PYTHON_VERSION := 3.11
BASE_DIR                   := $(shell pwd)

# executables
GIT_LOCAL     := $(call shell_variable, git)
PYTHON3_LOCAL := $(call shell_variable, python3)
VENV          := $(call shell_variable, virtualenv)
PIP3_LOCAL    := $(call shell_variable, pip3)
ifeq ($(call shell_variable, conda),)
CONDA_LOCAL   := ~/anaconda3/bin/conda
else
CONDA_LOCAL   := $(call shell_variable, conda)
endif


# venv executables

PYTHON3 	   := ~/anaconda3/envs/${VENV_NAME}/bin/python3
PIP3    	   := ~/anaconda3/envs/${VENV_NAME}/bin/pip3
PYSIDE6_UIC    := ~/anaconda3/envs/${VENV_NAME}/bin/pyside6-uic
PYINSTALLER    := ~/anaconda3/envs/${VENV_NAME}/bin/pyinstaller
PIP3_notConda  := ./${VENV_NAME}/bin/pip3
#----------------

#----------------
# recipes

setup-dirs:
	touch ${BASE_DIR}/__init__.py \
	      ${BASE_DIR}/README.md \
	      ${BASE_DIR}/requirements.txt \
	      ${BASE_DIR}/.gitignore

# check for prerequisites
check-dependencies: prerequisites := make bash python3 pip3 virtualenv conda
                    dependency_checker = $(if $(shell which $1), $(call info_logger, $2), $(call error_logger, $3))
check-dependencies:
	@$(foreach prerequisite, ${prerequisites}, \
	$(call dependency_checker, ${prerequisite}, ${prerequisite} installation found, ${prerequisite} installation not found))

compile-ui:
	@$(call info_logger, Converting .ui files to python code)
	@for file in ./frontend/assets/ui/*.ui ; do \
  		temp=$$(basename -- "$$file"); \
        ${PYSIDE6_UIC} $${file} -o ./frontend/"$${temp%.*}".py; \
    done

freeze-conda-requirements:
	@$(call info_logger, Freezing environment)
	${PIP3} list --format=freeze >> ${BASE_DIR}/requirements.txt
	awk -i inplace '!seen[$$0]++' requirements.txt

freeze-pip-requirements:
	@$(call info_logger, Freezing environment)
	${PIP3_notConda} list --format=freeze >> ${BASE_DIR}/requirements.txt
	awk -i inplace '!seen[$$0]++' requirements.txt

# syntax: make install-pip-package package="pyQT6"
install-pip-package:
	@$(call info_logger, Installing pip packages)
	${PIP3} install --no-cache-dir ${package}

prep-conda-virtual-environment:
	@$(call info_logger, Preparing python virtual environment)
	${CONDA_LOCAL} create --name ${VENV_NAME} python=${RECOMMENDED_PYTHON_VERSION} -y
	${CONDA_LOCAL} env list | grep "${VENV_NAME}"
	${PIP3} install -r ${BASE_DIR}/requirements.txt

build-dist: clean-build
	@$(call info_logger, Generating Build...)
	cd ${BASE_DIR}/frontend && \
	${PYINSTALLER} driver.py

app: prep-conda-virtual-environment
	@$(call info_logger, Starting up the app)
	cd ${BASE_DIR}/frontend && \
	${PYTHON3} driver.py

# cleanup
clean-virtualenv: garbage := "~/anaconda3/envs/${VENV_NAME}"
clean-virtualenv:
	@$(call info_logger, Cleaning python virtual environment)
	${CONDA_LOCAL} env remove --name ${VENV_NAME}
	@$(call garbage_collector, ${garbage})

clean-logs: garbage := "${BASE_DIR}/logs"
clean-logs:
	@$(call info_logger, Cleaning logs)
	@$(call garbage_collector, ${garbage})

clean-build: garbage := "${BASE_DIR}/frontend/build" "${BASE_DIR}/frontend/dist" "${BASE_DIR}/frontend/driver.spec"
clean-build:
	@$(call info_logger, Cleaning frontend build)
	@$(call garbage_collector, ${garbage})

# git
# syntax: make commit-push msg="My comment"
commit-push-master:
	${GIT_LOCAL} add .
	${GIT_LOCAL} commit -m "${msg}"
	${GIT_LOCAL} push origin master

master-to-main:
	${GIT_LOCAL} branch -m master main
	${GIT_LOCAL} push -u origin main
	${GIT_LOCAL} push origin --delete master
	${GIT_LOCAL} branch --delete master
	${GIT_LOCAL} checkout main
	${GIT_LOCAL} pull origin main

# master commands
clean: clean-logs clean-virtualenv
	@$(call info_logger, Master Janitor cleaned up your garbage.)
run-app: clean-virtualenv check-dependencies prep-virtual-environment app
final-check: check-dependencies prep-virtual-environment app clean commit-push-master