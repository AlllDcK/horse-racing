pipeline {

    agent any

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/AlllDcK/horse-racing'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t horse_racing .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python manage.py test'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker stop horse_racing_container || true'
                sh 'docker rm horse_racing_container || true'

                sh '''
                docker run -d \
                --name horse_racing_container \
                -p 8000:8000 \
                horse_racing
                '''
            }
        }
    }
}