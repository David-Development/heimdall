# xenial = 16.04
# zesty  = 17.04
# artful = 17.10
FROM ubuntu:xenial 

RUN apt-get update \
    && apt-get install -y cmake pkg-config \
    && apt-get install -y libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev \
    && apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev \
    && apt-get install -y libgtk-3-dev libatlas-base-dev gfortran libboost-all-dev \
    && apt-get install -y wget unzip \
    && apt-get install -y python2.7-dev python-tk python-pip \
    && pip install --upgrade pip \
    && pip install numpy psycopg2 \
    && rm -rf /var/lib/apt/lists/*

ENV opencv_version=3.3.0

RUN mkdir ~/opencv \
    && cd ~/opencv \
    && wget -O opencv.zip https://github.com/opencv/opencv/archive/${opencv_version}.zip \
    && wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/${opencv_version}.zip \
    && unzip opencv.zip \
    && unzip opencv_contrib.zip \
    && cd opencv-${opencv_version}/ \
    && mkdir build \
    && cd ~/opencv/opencv-${opencv_version}/build/ \
    && cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        #-D WITH_TBB=ON \
        #-D WITH_EIGEN=ON \
        #-D WITH_CUDA=ON \
        -D ENABLE_FAST_MATH=1 \
        #-D CUDA_FAST_MATH=1 \
        #-D WITH_CUBLAS=1 \
        #-D INSTALL_PYTHON_EXAMPLES=ON \
        -D BUILD_PYTHON_SUPPORT=ON \
        #-D BUILD_SHARED_LIBS=OFF \
        -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-${opencv_version}/modules \
        #-D BUILD_EXAMPLES=ON \
        .. \
    && make -j4 \
    && make install \
    && ldconfig \
    && rm -rf ~/opencv/*

#RUN cd ~/envs/<virtuelenv>/lib/python2.7/site-packages/ \
#    && ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so

#WORKDIR /app/

#RUN mkdir -p app/ml_models \
#    && cd app/ml_models \
#    && wget https://github.com/davisking/dlib-models/raw/master/dlib_face_recognition_resnet_model_v1.dat.bz2 \
#    && wget https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2 \
#    && bunzip2 dlib_face_recognition_resnet_model_v1.dat.bz2 \
#    && bunzip2 shape_predictor_68_face_landmarks.dat.bz2
#    #&& rm dlib_face_recognition_resnet_model_v1.dat.bz2 \
#    #&& rm shape_predictor_68_face_landmarks.dat.bz2

# copy the requirements file over
COPY ./heimdall/requirements.txt requirements.txt
RUN pip install -U -r requirements.txt \
    && rm requirements.txt

VOLUME ["/app"]
WORKDIR /app/

# Copy the files over
#COPY ./heimdall/ .

#RUN mv app/default_config_docker.py app/default_config.py

#ENV PYTHONIOENCODING=utf8

RUN apt-get update \
    && apt-get install -y htop

#CMD /bin/bash -c "ls -la /usr/local/lib/python2.7/site-packages/ ; ls -la ~/opencv/opencv-3.3.0/build/lib/"
CMD /bin/bash -c "sh startDocker.sh"
#CMD /bin/bash -c "celery worker --detach -A celery_worker.celery --loglevel=info; python manage.py run"