# xenial = 16.04
# zesty  = 17.04
# artful = 17.10
FROM ubuntu:xenial 


# Set the locale to support proper utf-8 encoding in Python3
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales && rm -rf /var/lib/apt/lists/*
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8


# Install Python3, Pip, Numpy, wget and unzip
RUN apt-get update \
    && apt-get install -y python3-dev python3-pip python3-numpy wget unzip \
    && python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir numpy \
    && rm -rf /var/lib/apt/lists/*

ENV opencv_version=3.4.1

# Install all requirements for opencv
RUN apt-get update \
    && apt-get install -y cmake pkg-config \
    && apt-get install -y libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev \
    && apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev \
    && apt-get install -y libgtk-3-dev libatlas-base-dev gfortran libboost-all-dev


RUN mkdir ~/opencv \
    && cd ~/opencv \
    && wget -O opencv.zip https://github.com/opencv/opencv/archive/${opencv_version}.zip \
    && wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/${opencv_version}.zip \
    && cd ~/opencv \
    && unzip opencv.zip \
    && unzip opencv_contrib.zip  \
    && cd ~/opencv/opencv-${opencv_version}/ \
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
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D BUILD_PYTHON_SUPPORT=ON \
        #-D BUILD_SHARED_LIBS=OFF \
        -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-${opencv_version}/modules \
        #-D BUILD_EXAMPLES=ON \
        .. \
    && make -j8 \
    && make install \
    && ldconfig \
    && rm -rf ~/opencv/*

#RUN apt-get purge -y cmake \
#    && apt-get autoremove -y \
#    && rm -rf /var/lib/apt/lists/*

WORKDIR /

# Test OpenCV Python Installation
RUN echo 'import cv2\n\
print("OpenCV Version: %s" % cv2.__version__)\n\
\n'\
>> /test.py \
    && python3 /test.py \
    && rm /test.py