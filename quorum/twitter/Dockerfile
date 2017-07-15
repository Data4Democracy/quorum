FROM alejandrox1/ubuntu_miniconda

RUN apt-get update -y
RUN pip install tweepy
RUN pip install kafka==1.3.3
COPY config.py /app/config.py
COPY twitter_api_users.py /app/twitter_api_users.py
WORKDIR /app

ENTRYPOINT ["python", "twitter_api_users.py"]

