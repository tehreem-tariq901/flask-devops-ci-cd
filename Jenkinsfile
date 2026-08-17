pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out project code'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Flask Docker image'
                sh 'docker build -t flask-devops-app .'
            }
        }

        stage('Validate Compose') {
            steps {
                echo 'Validating Docker Compose configuration'
                sh 'docker compose config -q'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application with Docker Compose'
                sh 'docker compose up -d'
            }
        }
    }
}
