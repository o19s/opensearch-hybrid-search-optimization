FROM python:3.12.6

COPY ./requirements.txt /code/requirements.txt
COPY ./model/regression_model.pkl /code/model/regression_model.pkl
#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

# Run the API
WORKDIR /code/app

#RUN fastapi run opensearch_inference_service.py
CMD ["fastapi", "run", "opensearch_inference_service.py"]
#CMD ["gunicorn", "main:app", "-b", "0.0.0.0:8000", "--timeout", "600", "-w", "1", "-k", "uvicorn.workers.UvicornWorker"]
EXPOSE 8000