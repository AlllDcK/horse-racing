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
                sh 'docker run -d -p 8000:8000 horse_racing'
            }
        }
    }
}