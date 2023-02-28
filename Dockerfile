FROM python:3.11-alpine
EXPOSE 8080

WORKDIR /api
COPY . /api

RUN pip install -r /api/requirements.txt

CMD ["uvicorn", "src.app:app"]
