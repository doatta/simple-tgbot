SHELL = /bin/bash

all: install start
dev: install_dev start
TOKEN := ""

prepare:
	@echo "#################################################"
	@echo "Preparing environment: installing mise and poetry"
	@echo "#################################################"
	@if ! which mise; then\
		curl https://mise.run | sh ;\
		echo 'eval "$$(~/.local/bin/mise activate bash)"' >> ~/.bashrc;\
		~/.local/bin/mise trust;\
	fi;
	@mise install

install:
	@echo
	@echo "#################################################################"
	@echo "Setting up environment for bot: installing only required packages"
	@echo "#################################################################"
	@echo
	@mise exec -- pip install poetry
	@mise exec -- poetry install

install_dev:
	@echo
	@echo "#######################################################"
	@echo "Setting up environment for bot: installing all packages"
	@echo "#######################################################"
	@echo
	@mise exec -- pip install poetry
	@mise exec -- poetry install --with dev

start:
	@echo
	@echo "################"
	@echo "Starting the bot"
	@echo "################"
	@echo
	@if [ -n $(TOKEN) ]; then\
		nohup mise exec -- poetry run tgbot -t $(TOKEN) & \
	else nohup mise exec -- poetry run tgbot &\
	fi



format:
	@mise exec -- black simple_tgbot

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	mise deactivate
	rm -rf .venv