FROM python:3.10

WORKDIR /diplom

COPY . /diplom

RUN pip install -r requirements.txt

ENV Api_shop 1

RUN python manage.py migrate


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "diplom.wsgi"]
