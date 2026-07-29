FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn dependency:go-offline -B
RUN mvn package -DskipTests
EXPOSE 8083
CMD ["java", "-jar", "target/search-service-0.1.0.jar"]
