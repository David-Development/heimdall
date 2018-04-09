# TLDR
Heimdall is an open source face recognition plattform. It's build on a microservice architecture based on docker and uses the powerful face recognition model from the [Dlib](https://github.com/davisking/dlib)-library by Davis King, 
as well as the Histogram of Oriented Gradients face detection model. Classification is done with a SVM classifier from 
[Scikit-Learn](http://scikit-learn.org/). It also features a native Android App as well as an WebInterface written in React. Installation Instructions can be found here: [Installation.md](Installation.md)

# Heimdall 
Heimdall is an open source face recognition plattform. It was designed especially to work with a peephole camera in order to recognize persons ringing the doorbell. This is not only very useful for people who are too lazy to get up just to know who is in front of their door, but also for elderly people that suffer from dementia. A first prototype of heimdall was created as part of the Masterthesis "Neuronale Netze und andere Verfahren zur Gesichtserkennung im Heimautomatisierungsfumeld" by Constantin Kirsch for the Master of Science in Computer Science at the Bonn-Rhine-Sieg University of Applied Sciences at the [Multimedia Communication Laboratory](http://mc-lab.inf.h-brs.de/).
This fork continous [his work](https://github.com/kircon/heimdall) by implementing a microservice architecture, several security features as well as improving the usability.
It uses the powerful face recognition model from the [Dlib](https://github.com/davisking/dlib)-library by Davis King, 
as well as the Histogram of Oriented Gradients face detection model. Classification is done with a SVM classifier from 
[Scikit-Learn](http://scikit-learn.org/). The face detection, feature extraction and training is embedded into a 
[Flask](http://flask.pocoo.org/) based Webapplication.
  
 
# Installation & Usage
Installation and Usage Instructions can be found in the [corresponding Installation instructions](Installation.md). If you have docker installed it's basically only one command.


# TODO

- UI
  - [ ] Improve visibility of progressbar in React App (training progress)
  - [ ] Blue mark stays on even after classifying an image 
  - [ ] Improve instructions on what to do after opening the timeline
  - [ ] LiveView - naming is misleading/confusing - change to something like "DetectionView"?
  - [ ] Reload page when clicking on the icon in the sidebar (if the page is already open the page won't reload)
  - [ ] [Update API access](https://github.com/David-Development/heimdall-frontend/blob/1332d96939c2f3101c0526444840a3ca83d09130/src/management/Classification.js#L187) to use the getImageUrl from HTTPClient 
  - [ ] only show images with one person (in classification view)
- [ ] remove heimdall-backend, heimdall-frontend and emq-docker dependency from this repo (the images are included via dockerhub - dependency is only used for debugging purposes)
- [ ] Implement some kind of housekeeping operation (delete old images) e.g.
  - after a training delete all images (good for performance)
  - delete images that are older than 10 days
  - keep 100 (unclassified) images
- [ ] Disable redis public port
- [ ] [Facial blur detection](https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/) - Remove blurry images (difficult to implement since amount of blur depends on many factors)
- [ ] Write frontend tests (read readme in heimdall-frontend for information on react testing)
- [x] Test resized images from API / Add special api for resized images
- [x] Check exposed ports in [Dockerfiles / Docker-Compose](https://stackoverflow.com/a/22150099)
- [x] Cleanup backend (Remove unused imports / Refactor code)
- [x] Better error handling (Push error messages to the client)
- [x] Use EMQ - MQTT Broker [EMQTT](http://emqtt.io/)
  - [Docker Container](https://github.com/emqtt/emq-docker)
  - [Example of sending images from RPI via MQTT](https://www.hackster.io/robin-cole/pi-camera-doorbell-with-notifications-408d3d)
- [x] API Endpoint /events very slow
- [x] Update Mosquitto to 1.4.14
- [x] Use [paho-mqtt](https://pypi.python.org/pypi/paho-mqtt/1.1) in backend and browser
- [x] Setup nginx in front of backend ([flask](https://flask-socketio.readthedocs.io/en/latest/))
- [x] Informationen in Android-App sollen nach 5min verschwinden
- [x] Weißer Rand am unteren Bildschirmrand in Webseite. Sonst sieht es so aus, als ob es noch weiter ginge
- [x] Automatisch zu angeklicktem Bild springen (und nicht zu erstem aus dem Event)
- [x] Beim Anlegen der Person diese auch automatisch markieren
- [x] Bilder laden geht nicht immer korrekt!! (In der Klassifizierungsansicht) (image key is missing)
- [x] Löschen einer Klassifikation löschen können (nochmal auf Namen drücken können um ein Bild löschen zu können)
- [x] Gallerie --> Popup einbauen und Bilder entfernen können --> Und neu zuordnen können


- Use VisualStudio [debugger-for-chrome](https://marketplace.visualstudio.com/items?itemName=msjsdiag.debugger-for-chrome)

