pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_TYPE',
            choices: ['api', 'ui', 'all'],
            description: 'Выберите тип тестов для запуска'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
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
                script {
                    def pytest_cmd = "python -m pytest --alluredir=allure-results"

                    // Формируем маркер в зависимости от выбора
                    def marker = params.TEST_TYPE == 'api' ? 'api' :
                                 params.TEST_TYPE == 'ui'  ? 'ui'  : ''

                    if (marker) {
                        pytest_cmd += " -m ${marker}"
                    }

                    withCredentials([
                        usernamePassword(
                            credentialsId: 'petrovich_cred',
                            usernameVariable: 'EMAIL',
                            passwordVariable: 'PASSWORD'
                        ),
                        string(
                            credentialsId: 'petrovich_cookies',
                            variable: 'COOKIES'
                        )
                    ]) {
                        sh ". venv/bin/activate && ${pytest_cmd}"
                    }
                }
            }
        }
    }

    post {
        always {
            allure(
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']],
                report: 'allure'
            )
        }
    }
}