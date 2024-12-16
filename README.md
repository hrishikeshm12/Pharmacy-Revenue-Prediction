
# 📈 Pharmacy Revenue Prediction System

Welcome to the **Pharmacy Revenue Prediction System**! This full-stack application leverages machine learning models to predict pharmacy revenue based on various input attributes. It's built with a Flask web application and a Java-based backend, containerized using Docker, and utilizes GitHub Actions for CI/CD pipeline automation.

![image](https://github.com/user-attachments/assets/ee67a4cf-1a7a-4ebc-89e6-171cec4e23f7)


## 🌟 Features
- **Flask Web Application**: Handles user requests, data processing, and interactions with backend services.
- **Java Backend**: Provides machine learning-based predictions to calculate pharmacy revenue.
- **Dockerized Application**: Fully containerized using Docker for portability and easy deployment.
- **CI/CD with GitHub Actions**: Automated builds and pushes Docker images to Docker Hub on code changes, ensuring reliable and fast deployments.
- **Easy Deployment**: Can be deployed on any cloud platform or local machine.

## 🛠 Tech Stack
- **Flask**: A lightweight WSGI web application framework in Python.
- **Java (Spring Boot)**: Backend API built in Java to handle complex logic and predictions.
- **Docker**: Containerization for easy distribution and deployment.
- **GitHub Actions**: CI/CD pipeline for automated testing, building, and pushing Docker images.
- **Docker Hub**: Hosting platform for Docker images.

## 📋 Prerequisites
Ensure you have the following installed on your local machine:
- Docker (for running containers)
- Docker Compose
- Git
- GitHub Account (for accessing the repository and CI/CD integration)
- Docker Hub Account (to push/pull images)

## 📁 Project Structure
```yaml
/project-root
  |-- /flask-app
  |    |-- Dockerfile
  |    |-- app.py
  |-- /java-backend
  |    |-- Dockerfile
  |    |-- Main.java
  |-- docker-compose.yml
  |-- .github/
       |-- workflows/
           |-- ci-cd-pipeline.yml
```
- /flask-app: Contains the Flask web application.
- /java-backend: Contains the Java backend API.
- docker-compose.yml: Defines the multi-container setup for Flask and Java services.
- /.github/workflows/ci-cd-pipeline.yml: GitHub Actions CI/CD configuration.

## 🚀 How to Use
1. Clone the Repository
```
git clone https://github.com/your-username/your-repo.git
cd your-repo
```
2. Build and Run Containers Locally
Ensure you have Docker and Docker Compose installed on your machine.
```
docker-compose up --build
```
- Flask App: http://localhost:5000

- Java Backend: http://localhost:8080

3. Push Docker Images to Docker Hub
```
git add .
git commit -m "Updated Dockerfiles"
git push origin main
```
The GitHub Actions pipeline will automatically:

- Build the Docker images for both the Flask app and Java backend.

- Push the Docker images to Docker Hub under your account.

## 🔄 CI/CD Pipeline with GitHub Actions
**GitHub Actions Workflow**

***Trigger***: Automatically on push to the main branch or manually via workflow_dispatch.

***Build***: Builds Docker images for Flask and Java backend.

***Push***: Pushes images to Docker Hub.

***Deploy***: Pulls latest Docker images and deploys the app.

**Monitor the Workflow**

- Go to the Actions tab in GitHub.
- Click on the most recent workflow run to see logs and monitor progress.

## 📦 Pull Docker Images

```
docker pull hrish06062001/flask-app:latest
docker pull hrish06062001/java-backend:latest
```
To start both containers:
```
docker-compose up
```

## 🎉 Conclusion
The Pharmacy Revenue Prediction System is a powerful and scalable solution to predict pharmacy revenues, leveraging a fully containerized architecture. With Docker, GitHub Actions, and Docker Hub, deployment and scalability are streamlined.

Feel free to contribute or use this project for your needs. Encounter any issues? Open an issue in the GitHub repository or reach out!

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

> Developed by Hrishikesh Magadum





