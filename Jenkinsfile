pipeline {
 agent any
   stages {
     stage('Setup Parameters') {
       steps {
         script {
            properties([
                githubProjectProperty(displayName: '', projectUrlStr: 'https://github.com/astronomer/cs-cicd-demo/'),
                parameters([string(defaultValue: 'RmUkDHvhaCSMKeLAHejhxGdebOz4M0hb', name: 'ASTRONOMER_KEY_ID'),
                string(defaultValue: 'gExNgKtTlQtJixXRn31do6qzSB9UIFlllqMAOwu6TYFN_uUlX6ISH36iprg9SseB', name: 'ASTRONOMER_KEY_SECRET'),
                string(defaultValue: 'cl4xce7dx500201bzlxbveud5c', name: 'DEPLOYMENT_ID')]),
                pipelineTriggers([githubPush()])
            ])
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