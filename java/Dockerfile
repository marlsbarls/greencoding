# syntax=docker/dockerfile:1

FROM openjdk:16-alpine3.13

WORKDIR /app

COPY . .

RUN javac Fibonacci.java
CMD ["java", "Fibonacci"]