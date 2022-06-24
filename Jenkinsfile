pipeline {
    agent {
        docker {
            image 'ubuntu'
            args '-u root:sudo -v $HOME/workspace/Astronomer CICD:/Astronomer CICD'
        }
    }
    stages {
      stage('Deploy to Astronomer') {
       when {
        expression {
          return env.GIT_BRANCH == "origin/main"
        }
       }
       steps {
         script {
               sh "curl -sSL install.astronomer.io | sudo bash -s"
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
