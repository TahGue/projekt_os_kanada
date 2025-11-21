.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	python -m src.dashboard

test:
	pytest tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
