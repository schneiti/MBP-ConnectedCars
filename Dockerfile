FROM openjdk:11-jre

RUN mkdir -p /usr/src/app
COPY target/MBP.jar /usr/src/app
WORKDIR /usr/src/app

CMD ["java", "-jar", "-Dspring.profiles.active=docker", "MBP.jar"]
