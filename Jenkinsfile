pipeline {
 agent any
   stages {
     stage('Set Environment Variables') {
       when {
        expression {
          return (env.GIT_BRANCH == "origin/main" || env.GIT_BRANCH == "origin/dev")
        }
       }
        steps {
            script {
                if (env.GIT_BRANCH == 'origin/main') {
                    echo "The git branch is ${env.GIT_BRANCH}";
                    env.ASTRONOMER_KEY_ID = env.PROD_ASTRONOMER_KEY_ID;
                    env.ASTRONOMER_KEY_SECRET = env.PROD_ASTRONOMER_KEY_SECRET;
                    env.DEPLOYMENT_ID = env.PROD_DEPLOYMENT_ID;
                } else if (env.GIT_BRANCH == 'origin/dev') {
                    echo "The git branch is ${env.GIT_BRANCH}";
                    env.ASTRONOMER_KEY_ID = env.DEV_ASTRONOMER_KEY_ID;
                    env.ASTRONOMER_KEY_SECRET = env.DEV_ASTRONOMER_KEY_SECRET;
                    env.DEPLOYMENT_ID = env.DEV_DEPLOYMENT_ID;
                } else {
                    echo "This git branch ${env.GIT_BRANCH} is not configured in this pipeline."
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