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
                    def pytest_cmd = "python -m pytest --alluredir=${env.ALLURE_RESULTS_DIR} -v"

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

        stage('Generate Report Image') {
            steps {
                script {
                    // Парсим результаты из allure-results
                    def total = 0
                    def passed = 0
                    def failed = 0
                    def skipped = 0

                    // Простой способ: считаем файлы .json в allure-results
                    def resultsDir = sh(script: "find ${env.ALLURE_RESULTS_DIR} -name '*.json' | wc -l", returnStdout: true).trim().toInteger()
                    if (resultsDir > 0) {
                        // Используем Python-скрипт для точного парсинга
                        sh ". venv/bin/activate && python parse_allure_results.py --results-dir ${env.ALLURE_RESULTS_DIR} --output stats.json"
                        def stats = readJSON file: 'stats.json'
                        total = stats.total
                        passed = stats.passed
                        failed = stats.failed
                        skipped = stats.skipped
                    } else {
                        // fallback
                        total = 1
                        passed = 1
                    }

                    // Сохраняем в env для использования в post
                    env.TOTAL_TESTS = total.toString()
                    env.PASSED_TESTS = passed.toString()
                    env.FAILED_TESTS = failed.toString()
                    env.SKIPPED_TESTS = skipped.toString()

                    // Генерируем изображение
                    def duration = currentBuild.durationString
                    duration = duration.replace(' and counting', '').replace(' and', '').replace(' ms', '').trim()

                    sh """
                        . venv/bin/activate
                        python generate_report_image.py \\
                            --passed ${passed} \\
                            --failed ${failed} \\
                            --skipped ${skipped} \\
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
                def reportName = "allure-report-${params.TEST_TYPE}"
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: env.ALLURE_RESULTS_DIR]],
                    report: reportName
                ])

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
                        // fallback: текстовое сообщение
                        def message = "✅ Тесты завершены!\\nТип: ${params.TEST_TYPE}\\n\\n❌ Не удалось сгенерировать изображение.\\n🔗 Отчёт: ${reportUrl}"
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
}