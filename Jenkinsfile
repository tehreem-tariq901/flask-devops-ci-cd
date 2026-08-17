pipeline {

    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                echo 'Building Flask Docker image'
                sh 'docker build -t flask-devops-app .'
            }
        }

        stage('Validate Compose') {
            steps {
                echo 'Validating Docker Compose configuration'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'mysql-credentials',
                        usernameVariable: 'MYSQL_USER',
                        passwordVariable: 'MYSQL_PASSWORD'
                    ),
                    string(
                        credentialsId: 'mysql-root-password',
                        variable: 'MYSQL_ROOT_PASSWORD'
                    )
                ]) {
                    sh '''
                        export MYSQL_DATABASE="tehreem"
                        docker compose config -q
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application with Docker Compose'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'mysql-credentials',
                        usernameVariable: 'MYSQL_USER',
                        passwordVariable: 'MYSQL_PASSWORD'
                    ),
                    string(
                        credentialsId: 'mysql-root-password',
                        variable: 'MYSQL_ROOT_PASSWORD'
                    )
                ]) {
                    sh '''
                        export MYSQL_DATABASE="tehreem"
                        docker compose up -d
                    '''
                }
            }
        }
    }
}
