FROM selenium/standalone-chrome

RUN sudo mkdir /usr/src/app
ADD . /usr/src/app/
WORKDIR /usr/src/app

RUN sudo apt update && sudo apt install -y python2
RUN sudo curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
RUN sudo python2 get-pip.py
RUN sudo apt-get -qq -y install  libxpm4 libxrender1 libgtk2.0-0 libnss3\ 
       libgconf-2-4  libpango1.0-0 libxss1 libxtst6 fonts-liberation\ 
       libappindicator1 xdg-utils
RUN sudo apt-get -y install \
               xvfb gtk2-engines-pixbuf \
               xfonts-cyrillic xfonts-100dpi xfonts-75dpi xfonts-base xfonts-scalable \
               imagemagick x11-apps zip

VOLUME /dev/shm:/dev/shm

EXPOSE 4444:4444

RUN sudo pip2 install --no-cache-dir -r requirements.txt

ENTRYPOINT python2 -m unittest -v Task2_test
