## Devops & SRE - Infrastructure library powered by AWS CDK
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
npm install -g aws-cdk@2.175.1
```

### Project setup 

```shell
python3 -m venv .venv 
```
```shell
source .venv/bin/activate 
```
```shell
python -m pip install -r requirements.txt
```
```shell
python -m pip install -r requirements-dev.txt
```

### Running tests
```shell
python -m pytest
```

### Running tests with coverage
```shell
python -m pytest --cov=tests
```

### Running tests with coverage (load environment variables before)
```shell
python -m pytest --cov=tests
```

### CDK - List the stacks in the app

```shell
cdk ls
```

### CDK - Synthesize an AWS CloudFormation template

```shell
cdk synth
```

### CDK - Diff

```shell
cdk diff
```


### CI/CD

Project pipeline: [CircleCI](https://app.circleci.com/pipelines/github/<your-company>/infra-awscdk-devops-packages)

### Publishing new release
Update the **version** in the files:
* setup.py and 
* .circleci/config.yml 

Create a tag release, where **version** format is vX.X.X Example: v1.0.6
```shell
git tag -fa "release/<version>" -m "Release <version>" && git push --tag --force
```

### Releases
https://manage.fury.io/dashboard/<your-company>/package/pkg_2kunmv/versions

