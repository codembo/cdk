# infra-awscdk-experiencia-nidera-packages
The devops packages using AWS CDK

### Install node

```shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

```shell
nvm install 20.0.0
```

### Install AWS CDK cli

```shell
npm install -g aws-cdk@2.160.0
```

### Project setup 

```shell
python3 -m venv .venv 
```
```shell
source .venv/bin/activate 
```
```shell
 export FURY_AUTH=<your-gemfury-access-token>
```
```shell
python -m pip install -r requirements.txt
```
```shell
python -m pip install -r requirements-dev.txt
```
### Environment variables setup using dotenv
```shell
pip install "python-dotenv[cli]"
```

### Running tests

```shell
dotenv --file .env.qa run python -m pytest
```

### Running tests with coverage
```shell
dotenv --file .env.qa run python -m pytest --cov=tests
```

### Running tests with coverage (load environment variables before)
```shell
dotenv --file .env.qa run python -m pytest --cov=tests
```

### CDK - List the stacks in the app

```shell
dotenv --file .env.qa run cdk ls
```

### CDK - Synthesize an AWS CloudFormation template

```shell
dotenv --file .env.qa run cdk synth
```

### CDK - Diff

```shell
dotenv --file .env.qa run cdk diff
```


### CI/CD

Project pipeline: [CircleCI](https://app.circleci.com/pipelines/github/<your-company>/infra-awscdk-devops-packages)

### Deployment
In order to deploy the application to QA, you need to run the following command:

```shell
./scripts/publish.sh -t [major|minor|patch]
```

To define the kind of release, you can use the following options:

- **major version**: increment when you make incompatible infra changes;
- **minor version**: increment when you add functionality in a backwards compatible manner;
- **patch version**: increment when you make backwards compatible bug fixes, compliance and performance improvements.

In order to deploy new infrastructure to *Production* approve the hold in the circleci pipeline.