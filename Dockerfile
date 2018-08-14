FROM python:3
COPY . /app
WORKDIR /app

ARG ASSEMBLY_TOKEN
ARG PROJECT_ID
ARG DATASET
ARG SANITY_TOKEN


RUN pip install -r requirements.txt
EXPOSE 8006
CMD ["python", "run.py"]