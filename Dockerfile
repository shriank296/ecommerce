FROM --platform=linux/arm64 python:3.12.0

WORKDIR /project

RUN pip install poetry==1.8.4 && poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /project/

RUN poetry install --no-root

ADD . .

CMD ["uvicorn", "source.app.adapter.fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]