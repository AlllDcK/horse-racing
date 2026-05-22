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
                bat 'docker build -t horse_racing .'
            }
        }

        stage('Run Tests') {

            steps {
                bat 'python manage.py test'
            }
        }

        stage('Run Container') {

            steps {
                bat 'docker run -d -p 8000:8000 horse_racing'
            }
        }
    }
}
