pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_TYPE',
            choices: ['api', 'ui', 'all'],
            description: 'Выберите тип тестов для запуска'
        )
    }

    environment {
        ALLURE_RESULTS_DIR = "${params.TEST_TYPE == 'all' ? 'allure-results/all' : "allure-results/${params.TEST_TYPE}"}"
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
                    sh "mkdir -p ${env.ALLURE_RESULTS_DIR}"
                    def historyPath = "allure-report-${params.TEST_TYPE}/history"
                    if (fileExists(historyPath)) {
                        sh "cp -r ${historyPath} ${env.ALLURE_RESULTS_DIR}/"
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def pytest_cmd = "python -m pytest --alluredir=${env.ALLURE_RESULTS_DIR}"

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
            script {
                def reportName = "allure-report-${params.TEST_TYPE}"
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: env.ALLURE_RESULTS_DIR]],
                    report: reportName
                ])

                def telegramToken = ''
                def chatId = '731627096'
                def message = "✅ Тесты завершены!\nТип: ${params.TEST_TYPE}\n"


                if (currentBuild.result == 'SUCCESS') {
                    message += "Статус: PASSED ✅"
                } else if (currentBuild.result == 'UNSTABLE') {
                    message += "Статус: UNSTABLE ⚠️"
                } else {
                    message += "Статус: FAILED ❌"
                }

            def reportUrl = env.BUILD_URL?.trim()
            if (!reportUrl.startsWith('http')) {
                reportUrl = "https://" + reportUrl
            }
            reportUrl = reportUrl.endsWith('/') ? reportUrl : reportUrl + '/'
            reportUrl += "allure"

            message += "\n\n📊 [Отчёт Allure](${reportUrl})"

                withCredentials([string(credentialsId: 'telegram_bot_token', variable: 'TELEGRAM_TOKEN')]) {
                    sh """
                        curl -s -X POST "https://api.telegram.org/bot\${TELEGRAM_TOKEN}/sendMessage" \\
                             -H "Content-Type: application/json" \\
                             -d '{
                                   "chat_id": "${chatId}",
                                   "text": "${message}",
                                   "parse_mode": "Markdown"
                                 }'
                    """
                }
            }
        }
    }
}