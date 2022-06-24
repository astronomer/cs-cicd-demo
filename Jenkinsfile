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
               sh 'curl https://github.com/astronomer/astro-cli/releases/download/v1.1.0/astro_1.1.0_linux_arm64.tar.gz -o astrocli.tar.gz'
               sh 'tar xzf astrocli.tar.gz'
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
