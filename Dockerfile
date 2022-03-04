FROM python:3.10-slim

RUN pip install poetry

WORKDIR /code

# install psycopg2 dependencies
RUN apt update \
    && apt install \
#    postgresql \
    gcc \
#    python3-dev \
#    musl-dev \
    libpq-dev -y

COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false && poetry install

COPY . /code

CMD ./manage.py runserver

#RUN pip install -r requirements.txt
#RUN pip install gunicorn

#COPY ./app ./app
#COPY ./templates ./templates
##COPY ./data ./data
#COPY run.py .
#COPY README.md .
#CMD gunicorn run:app -b 0.0.0.0:80

#RUN apt update && apt install -y python