pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Prepare Allure History') {
            steps {
                script {
                    sh 'mkdir -p allure-results'
                    if (fileExists('allure-report/history')) {
                        sh 'cp -r allure-report/history allure-results/'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'source venv/bin/activate && python -m pytest --alluredir=allure-results'
            }
        }
    }

    post {
        always {
            allure(
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            )
        }
    }
}