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
               sh 'sudo apt-get install bash'
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
