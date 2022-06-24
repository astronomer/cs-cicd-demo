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
               sh "sudo chown root:jenkins /run/docker.sock"
               sh 'curl -sSL install.astronomer.io | bash -s'
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
