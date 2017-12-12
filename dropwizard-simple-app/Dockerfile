FROM openjdk:latest

RUN apt-get update && apt-get install -y maven

COPY pom.xml pom.xml
COPY src src

RUN mvn -T 1C clean package

COPY example.keystore .
COPY example.yml .

CMD ["java", "-jar", "target/dropwizard-simple-app-0.1.jar", "server", "example.yml"]
