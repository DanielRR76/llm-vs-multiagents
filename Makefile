compose-up:
	docker compose -f docker/docker-compose.yml up -d --build

compose-down:
	docker compose -f docker/docker-compose.yml down -v

exec-llm:
	docker compose -f docker/docker-compose.yml exec llm bash

llm-install:
	pip install -r requirements.txt && cd src/environment/python && pip install -r requirements.txt

llm-run:
	PYTHONPATH=. streamlit run src/main.py

python-test:
	pytest src/environment/python/tests/test_input_code.py

python-coverage-json:
	pytest --cov=src/environment/python src/environment/python/tests/test_input_code.py --cov-report=json:src/environment/python/coverage.json --cov-branch

python-cov:
	pytest --cov=src/environment/python/app src/environment/python/tests/test_input_code.py --cov-branch

python-mut:
	cd src/environment/python && mutmut run
