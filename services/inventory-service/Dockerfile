FROM eclipse-temurin:17-jdk-alpine
ARG SERVICE_PATH=.
WORKDIR /app
COPY ${SERVICE_PATH}/pom.xml .
COPY shared/java-common-lib/pom.xml shared/java-common-lib/
COPY shared/java-common-lib/src shared/java-common-lib/src
RUN mvn -f shared/java-common-lib/pom.xml install -DskipTests
COPY ${SERVICE_PATH}/src ./src
RUN mvn dependency:go-offline -B
RUN mvn package -DskipTests
EXPOSE 8082
CMD ["java", "-jar", "target/$(basename ${SERVICE_PATH})-0.1.0.jar"]
