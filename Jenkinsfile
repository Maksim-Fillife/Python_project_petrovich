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
        REPORT_IMAGE = "report_${params.TEST_TYPE}.png"
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

        stage('Run Tests') {
            steps {
                script {
                    def pytest_cmd = "python -m pytest --alluredir=${env.ALLURE_RESULTS_DIR}"

                    def marker = params.TEST_TYPE == 'api' ? 'api' :
                                 params.TEST_TYPE == 'ui'  ? 'ui'  : ''

                    if (marker) {
                        pytest_cmd += " -m ${marker}"
                    }

                    // Запуск с сохранением вывода для парсинга
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
                        sh ". venv/bin/activate && ${pytest_cmd} --tb=short -v > pytest_output.txt || true"
                    }
                }
            }
        }

        stage('Parse Test Results') {
            steps {
                script {
                    // Простой парсинг из вывода pytest
                    def output = readFile('pytest_output.txt')
                    def passed = (output =~ /(\d+) passed/).size() > 0 ? (output =~ /(\d+) passed/)[0][1].toInteger() : 0
                    def failed = (output =~ /(\d+) failed/).size() > 0 ? (output =~ /(\d+) failed/)[0][1].toInteger() : 0
                    def skipped = (output =~ /(\d+) skipped/).size() > 0 ? (output =~ /(\d+) skipped/)[0][1].toInteger() : 0

                    env.PASSED = passed.toString()
                    env.FAILED = failed.toString()
                    env.SKIPPED = skipped.toString()
                }
            }
        }

        stage('Generate Report Image') {
            steps {
                script {
                    def duration = currentBuild.durationString
                    duration = duration.replace(' and counting', '')
                                 .replace(' and', '')
                                 .replace(' ms', '')
                                 .trim()

                    sh """
                        . venv/bin/activate
                        python generate_report_image.py \\
                            --passed ${env.PASSED} \\
                            --failed ${env.FAILED} \\
                            --skipped ${env.SKIPPED} \\
                            --duration "${duration}" \\
                            --test-type "${params.TEST_TYPE}" \\
                            --output ${env.REPORT_IMAGE}
                    """
                }
            }
        }
    }

    post {
        always {
            script {
                // Генерация Allure-отчёта
                def reportName = "allure-report-${params.TEST_TYPE}"
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: env.ALLURE_RESULTS_DIR]],
                    report: reportName
                ])

                // Отправка в Telegram
                def chatId = '731627096'
                def reportUrl = "${env.BUILD_URL}allure"

                withCredentials([string(credentialsId: 'telegram_bot_token', variable: 'TELEGRAM_TOKEN')]) {
                    if (fileExists(env.REPORT_IMAGE)) {
                        sh """
                            curl -s -X POST "https://api.telegram.org/bot\${TELEGRAM_TOKEN}/sendPhoto" \\
                                 -F "chat_id=${chatId}" \\
                                 -F "photo=@${env.REPORT_IMAGE}" \\
                                 -F "caption=✅ Тесты завершены!\\nТип: ${params.TEST_TYPE}\\n\\n🔗 Отчёт: ${reportUrl}" \\
                                 -F "parse_mode=Markdown"
                        """
                    } else {
                        // fallback
                        sh """
                            curl -s -X POST "https://api.telegram.org/bot\${TELEGRAM_TOKEN}/sendMessage" \\
                                 -H "Content-Type: application/json" \\
                                 -d '{
                                       "chat_id": "${chatId}",
                                       "text": "✅ Тесты завершены!\\nТип: ${params.TEST_TYPE}\\n\\n❌ Не удалось создать изображение.\\n🔗 Отчёт: ${reportUrl}",
                                       "parse_mode": "Markdown"
                                     }'
                        """
                    }
                }
            }
        }
    }
}