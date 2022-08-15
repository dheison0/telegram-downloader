FROM python:3.10-alpine3.15
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
CMD ["python", "-m", "bot"]