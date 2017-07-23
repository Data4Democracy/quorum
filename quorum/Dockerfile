FROM alejandrox1/ubuntu_miniconda


RUN apt-get update -y
COPY . /app/
RUN pip install -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT ["python", "run_something.py"]

