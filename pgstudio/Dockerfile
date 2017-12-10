#FROM tomcat:8-jre8
FROM tomcat:8-alpine
MAINTAINER David Luhmer <david-dev@live.de>

WORKDIR $CATALINA_HOME/webapps/

RUN apk-add wget unzip \
    && wget http://downloads.postgresqlstudio.org/2.0/pgstudio_2.0.zip -O pgstudio_2.0.zip \
    && unzip pgstudio_2.0.zip && mv pgstudio.war ROOT.war && rm pgstudio_2.0.zip
WORKDIR $CATALINA_HOME
