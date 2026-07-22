// Healthekit Backend CI/CD — one pipeline, env chosen by branch/parameter
pipeline {
  agent any
  parameters {
    choice(name: 'DEPLOY_ENV', choices: ['dev', 'qa', 'uat', 'prod'], description: 'Target environment')
  }
  environment {
    IMAGE = "navistresundios/healthekit-backend"
    DOCKERHUB = credentials('dockerhub-navistresundios')     // Jenkins credential id
    GIT_SHA = "${env.GIT_COMMIT?.take(8)}"
    TAG = "${params.DEPLOY_ENV}-${env.BUILD_NUMBER}-${GIT_SHA}"
  }
  stages {
    stage('Lint & Test') {
      steps {
        sh '''
          python3 -m venv .venv && . .venv/bin/activate
          pip install -r requirements.txt -r requirements-dev.txt
          ruff check app tests
          pytest -q --cov=app --cov-report=term-missing
        '''
      }
    }
    stage('Build Image') {
      steps { sh 'docker build -t $IMAGE:$TAG .' }
    }
    stage('Push Image') {
      steps {
        sh '''
          echo $DOCKERHUB_PSW | docker login -u $DOCKERHUB_USR --password-stdin
          docker push $IMAGE:$TAG
          if [ "$DEPLOY_ENV" = "prod" ]; then docker tag $IMAGE:$TAG $IMAGE:latest && docker push $IMAGE:latest; fi
        '''
      }
    }
    stage('Deploy') {
      steps {
        // SSH to the env app box and roll the container. Host key + ssh key stored in Jenkins credentials.
        sshagent (credentials: ["healthekit-${params.DEPLOY_ENV}-ssh"]) {
          sh '''
            ssh -o StrictHostKeyChecking=accept-new ubuntu@$(cat /var/jenkins_home/hosts/${DEPLOY_ENV}-app.host)               "cd /opt/healthekit && export BACKEND_TAG=$TAG &&                docker compose -f docker-compose.${DEPLOY_ENV}.yml pull api &&                docker compose -f docker-compose.${DEPLOY_ENV}.yml up -d api && docker image prune -f"
          '''
        }
      }
    }
    stage('Smoke Test') {
      steps { sh 'sleep 10 && curl -sf https://api.${DEPLOY_ENV}.healthekit.in/healthz || (echo SMOKE FAIL && exit 1)' }
    }
  }
  post {
    always { cleanWs() }
  }
}
