test-no-docker:
	pip install uv \
	&& uv venv \
	&& . .venv/bin/activate \
	&& uv pip install -r requirements.txt

test:
	docker compose up --build

run:
	. .venv/bin/activate && python src/main.py
