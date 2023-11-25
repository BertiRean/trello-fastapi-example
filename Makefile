setup:
	python3.11 -m venv .venv

install:
	pip install -r requirements.txt

activate_windows:
	.\.venv\Scripts\activate

deactive_windows:
	.\.venv\Scripts\deactivate.bat

activate_unix:
	. .venv/bin/activate

clean:
	pyclean .

run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	black app && black tests
