FROM selenium/standalone-chrome

RUN mkdir /usr/src/app
ADD . /usr/src/app/
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y python-pip

VOLUME /dev/shm:/dev/shm
EXPOSE 4444:4444

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT  python testCase_testTask2.py