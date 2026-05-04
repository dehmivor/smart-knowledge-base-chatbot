.PHONY: install test run-backend run-frontend

install:
	cd backend && pip install -r requirements.txt -r requirements-dev.txt
	cd frontend && npm install

test:
	cd backend && pytest

run-backend:
	cd backend && python app/main.py

run-frontend:
	cd frontend && npm run dev
