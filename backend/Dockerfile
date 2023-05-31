FROM python:3.10.2
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . /code

RUN apt-get update && \
    pip install twisted[tls] h2 && \
    apt-get install -y python3-pip && \
    pip install -r requirements.txt


EXPOSE 8000

# Run the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]