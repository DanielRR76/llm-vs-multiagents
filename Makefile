compose-up:
	docker compose -f docker/docker-compose.yml up -d --build

compose-down:
	docker compose -f docker/docker-compose.yml down -v

exec-llm:
	docker compose -f docker/docker-compose.yml exec llm bash

llm-install:
	pip install -r requirements.txt

llm-run:
	PYTHONPATH=. streamlit run src/main.py

python-test:
	pytest src/environment/python/input_code_test.py

python-coverage:
	pytest --cov=src/environment/python src/environment/python/input_code_test.py --cov-report=json:src/environment/python/coverage.json

# 	pytest --cov=src/environment/python/input_code.py --cov-report=json:coverage.json

