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
               sh "curl -sSL install.astronomer.io"
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
