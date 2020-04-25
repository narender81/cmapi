FROM python:3.8-alpine
WORKDIR /app
COPY . .
CMD source ./venv/bin/activate
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD python3 app.py


