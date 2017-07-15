FROM alejandrox1/ubuntu_miniconda

RUN apt-get update -y
RUN pip install facebook-sdk
RUN pip install facepy
RUN pip install kafka==1.3.3
COPY config.py /app/config.py
COPY fb_api_pages.py /app/fb_api_pages.py
WORKDIR /app

ENTRYPOINT ["python", "fb_api_pages.py"]

