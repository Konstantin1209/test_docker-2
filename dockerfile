FROM python:latest

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .

RUN python manage.py migrate



EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "stocks_products.wsgi:application"]