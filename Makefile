SHELL = /bin/bash
WOKR_DIR = ./app

# install
install:
	@docker compose up -d

# run flask app
run-flask-app:
	docker image build -t flask-app flask-app/app/.
	docker run -d -p 8000:8080 -v ./flask-app/app:/app flask-app