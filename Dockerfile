FROM selenium/standalone-chrome

RUN sudo mkdir /usr/src/app
ADD . /usr/src/app/
WORKDIR /usr/src/app

RUN sudo apt update && sudo apt install -y python2
RUN sudo curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
RUN sudo python2 get-pip.py

VOLUME /dev/shm:/dev/shm

EXPOSE 4444:4444

RUN sudo pip2 install --no-cache-dir -r requirements.txt

ENTRYPOINT python -m unittest -v test_mail
