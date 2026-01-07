.PHONY: install dev test

dev:
	uvicorn emprunt.app:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -q
