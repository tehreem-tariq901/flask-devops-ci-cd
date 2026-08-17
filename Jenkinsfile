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
                echo 'Deploying MySQL and Flask application'

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

                        echo "Starting MySQL..."
                        docker compose up -d mysql

                        echo "Waiting for MySQL to become ready..."

                        until docker exec \
                            -e MYSQL_PWD="$MYSQL_PASSWORD" \
                            mysql-db \
                            mysqladmin ping \
                            -h 127.0.0.1 \
                            -u"$MYSQL_USER" \
                            --silent
                        do
                            sleep 2
                        done

                        echo "MySQL is ready."

                        echo "Checking database tables..."

                        TABLE_COUNT=$(docker exec \
                            -e MYSQL_PWD="$MYSQL_PASSWORD" \
                            mysql-db \
                            mysql \
                            -u"$MYSQL_USER" \
                            -N \
                            -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$MYSQL_DATABASE';")

                        if [ "$TABLE_COUNT" -eq 0 ]; then

                            echo "Database is empty. Importing SQL backup..."

                            docker cp \
                                docker-entrypoint-initdb.d/tehreem.sql \
                                mysql-db:/tmp/tehreem.sql

                            docker exec \
                                -e MYSQL_PWD="$MYSQL_PASSWORD" \
                                -e MYSQL_USER="$MYSQL_USER" \
                                -e MYSQL_DATABASE="$MYSQL_DATABASE" \
                                mysql-db \
                                sh -c 'mysql -u"$MYSQL_USER" "$MYSQL_DATABASE" < /tmp/tehreem.sql'

                            echo "Database import completed."

                        else

                            echo "Database already contains tables. Skipping SQL import."

                        fi

                        echo "Starting Flask..."

                        docker compose up -d flask

                        echo "Deployment completed."
                    '''
                }
            }
        }
    }
}
