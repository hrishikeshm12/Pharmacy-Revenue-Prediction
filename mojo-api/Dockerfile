# Dockerfile for Spring Boot app
FROM maven:3.8.1-openjdk-17 AS build

WORKDIR /app

COPY pom.xml .
COPY src/ ./src
RUN mvn clean package -DskipTests

FROM openjdk:17-slim

WORKDIR /app

COPY --from=build /app/target/*.jar app.jar
COPY models/ ./models

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
