SHELL = /bin/bash
WOKR_DIR = ./app

# install
install:
	@docker compose up -d

# run streamlit app
run-streamlit-app:
	docker image build -t streamlit-app streamlit-app/app/.
	docker run -d -p 8080:8080 -v ./streamlit-app/app:/app streamlit-app