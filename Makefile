.PHONY: install run test lint format clean

install:
	pip install -r backend/requirements.txt

run:
	cd backend && PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	cd backend && PYTHONPATH=. pytest -q

lint:
	cd backend && PYTHONPATH=. flake8 app tests

format:
	black backend/app backend/tests
	isort backend/app backend/tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
