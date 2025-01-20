## Devops & SRE - Infrastructure library examples
The examples of usage for devops packages

### Install node

```shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

```shell
nvm install 20.0.0
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

### Useful commands
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


