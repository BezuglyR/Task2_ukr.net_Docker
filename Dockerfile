FROM bezuglyr/pyhon2.7-chrome

RUN mkdir /usr/src/app
ADD . /usr/src/app/
WORKDIR /usr/src/app

VOLUME /dev/shm:/dev/shm

EXPOSE 4444:4444

RUN pip2 install --no-cache-dir -r requirements.txt

ENTRYPOINT python2 -m unittest -v Task2_test
