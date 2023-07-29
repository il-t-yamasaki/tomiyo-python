SHELL = /bin/bash
WOKR_DIR = ./app

# install
install:
	@docker compose up -d

# run sfastapi app
run-fastapi-app:
	docker image build -t fastapi-app fastapi-app/.
	docker run -d -p 80:80 fastapi-app