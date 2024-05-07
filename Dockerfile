###################
## Builder image ##
###################
FROM python:3.9 as builder

RUN pip3 install poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

# Install dependencies to venv
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt -o requirements.txt


###################
### Final image ###
###################
FROM python:3.9

WORKDIR /app

COPY --from=builder /app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY logging.yml /app/
COPY hookbridge /app/hookbridge/

CMD [ "uvicorn", "hookbridge.main:app", "--host", "0.0.0.0", "--port", "80" ]
