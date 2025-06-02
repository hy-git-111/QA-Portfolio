pipeline {
  agent {
    docker {
      image 'python:3.10'
      args '-u root'
    }
  }

  environment {
    PYTHONUNBUFFERED = '1'
  }

  stages {
    stage('연동 확인') {
      steps {
        echo '✅ GitLab에서 Jenkins로 연동 확인됨'
      }
    }

    stage('HTML 리포트 발행') {
      steps {
        publishHTML(target: [
          reportDir:   'reports',          // ★ 리포트가 있는 폴더
          reportFiles: 'report.html',      // ★ 파일 이름
          reportName:  'Test Report',      // 파이프라인에서 보일 제목
          keepAll:               true,     // 매 빌드마다 보존
          allowMissing:          false,    // 보고서가 없으면 빌드 실패
          alwaysLinkToLastBuild: true      // “Last successful build” 링크
        ])
      }
    }
  }

  stages {
    stage('Install Dependencies') {
      steps {
        sh 'pip install -r qa-realworld-automation/requirements.txt'
      }
    }

    stage('Run Tests') {
      steps {
        sh 'pytest qa-realworld-automation/tests --maxfail=1 --disable-warnings -v'
      }
    }
  }

  post {
    always {
      echo '📌 모든 단계 종료됨'
    }
    success {
      echo '🎉 테스트 성공'
    }
    failure {
      echo '❌ 테스트 실패 - 로그 확인 필요'
    }
  }
}
