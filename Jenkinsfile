pipeline {
 agent any
   stages {
     stage('Set Environment Variables') {
        steps {
            script {
                switch(env.GIT_BRANCH) {
                    case 'origin/dev' :
                        env.ASTRONOMER_KEY_ID = ${DEV_ASTRONOMER_KEY_ID};
                        env.ASTRONOMER_KEY_SECRET = ${DEV_ASTRONOMER_KEY_SECRET};
                        env.DEPLOYMENT_ID = ${DEV_DEPLOYMENT_ID};
                    case 'origin/main' :
                        env.ASTRONOMER_KEY_ID = ${PROD_ASTRONOMER_KEY_ID};
                        env.ASTRONOMER_KEY_SECRET = ${PROD_ASTRONOMER_KEY_SECRET};
                        env.DEPLOYMENT_ID = ${PROD_DEPLOYMENT_ID};
                }
            }
        }
     }
     stage('Deploy to Astronomer') {
       when {
        expression {
          return (env.GIT_BRANCH == "origin/main" || env.GIT_BRANCH == "origin/dev")
        }
       }
       steps {
         script {
           sh 'curl -LJO https://github.com/astronomer/astro-cli/releases/download/v1.1.0/astro_1.1.0_linux_amd64.tar.gz'
           sh 'tar xzf astro_1.1.0_linux_amd64.tar.gz'
           sh "./astro deploy ${DEPLOYMENT_ID} -f"
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
