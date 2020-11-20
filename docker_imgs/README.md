# OpenCV docker image

[Install OpenCV Docker Image on Ubuntu, MacOS or Windows](https://www.learnopencv.com/install-opencv-docker-image-ubuntu-macos-windows/)



```bash
docker pull spmallick/opencv-docker:opencv
```

To run the image: 
```bash
docker run --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -p 5000:5000 -p 8888:8888 -it spmallick/opencv-docker:opencv /bin/bash
```

```bash
docker run -p 5000:5000 -p 8888:8888 -it spmallick/opencv-docker:opencv bash
```


* –device=/dev/video0:/dev/video0 allows use of webcam
* -v /tmp/.X11-unix:/tmp/.X11-unix helps in X11 forwarding so that we can use functions like cv::imshow.
* -e is used to pass an environment variable.
* -it starts an interactive session
* -p sets up a port forward. This flag maps the container’s port to a port on the host system.
* /bin/bash runs .bashrc file on startup


# install open CV on ubuntu

(pip instal opencv)[https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/]