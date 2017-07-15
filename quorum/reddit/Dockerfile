FROM alejandrox1/ubuntu_miniconda

RUN apt-get update -y
RUN pip install praw 
RUN pip install kafka==1.3.3
COPY config.py /app/config.py
COPY reddit_api_subredits.py /app/reddit_api_subredits.py
WORKDIR /app

ENTRYPOINT ["python", "reddit_api_subredits.py"]


