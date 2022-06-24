pipeline {
    agent any
    stages {
      stage('Deploy to Astronomer') {
       when {
        expression {
          return env.GIT_BRANCH == "origin/main"
        }
       }
       steps {
         script {
               sh 'apk add --update curl && rm -rf /var/cache/apk/*'
               sh 'apk add bash'
               sh(script: 'curl -sSL install.astronomer.io | bash -s', returnStdout: true)
               sh 'astro deploy -f'
         }
       }
     }
   }
 post {
   always {
     cleanWs()
   }
  }
}
