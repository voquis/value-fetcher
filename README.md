# Value fetcher
## Introduction
Python module to fetch values from multiple sources with optional defaults, including:
- Environment variables
- AWS Systems Manager (SSM) Parameter Store
- AWS Secrets Manager

## Usage
Install the package with the following:

```shell
pip install value-fetcher
```

### Fetching values directly
In this use case, the value fetcher package makes it convenient to fetch values from the supported sources in a consistent and simplified manner.
```python
from value_fetcher import ValueFetcher

# Instantiate value fetcher class
fetcher = ValueFetcher()

# Retrieve values from supported AWS sources
my_secret = fetcher.get_from_aws_secrets_manager('/my/secret/key')
my_param = fetcher.get_from_aws_ssm_parameter_store('/my/parameter/key')
```

### Configuring source locations dynamically
In this use case, environment variables are used to configure the sources for multiple keys.
This is useful in more complex applications where lots of values need to be fetched and the source needs to be configured dynamically.
See this [contact form handler repository](https://github.com/voquis/aws-lambda-contact-form-handler) for example usage.

Environment variables can be appended to the configuration key name, setting the source of the value.
These are:
- `_PARAMETER_STORE_NAME` - for AWS SSM Parameter Store
- `_SECRETS_MANAGER_NAME` - for AWS Secrets Manager

One of the available configuration sources for each value must also be set by setting an environment variable ending with `_SOURCE` for the value name:
- `env` - Environment variables (default)
- `aws_ssm_parameter_store` - AWS Systems Manager (SSM) Parameter Store
- `aws_secrets_manager` - AWS Secrets Manager

For example, to fetch `MY_PARAM` from AWS SSM Parameter Store and `MY_SECRET` from AWS Secrets Manager, consider the following python script (e.g. `app.py`) called subsequently by a shell script:

```python
# This file is app.py for example
from value_fetcher import ValueFetcher

# Instantiate value fetcher class, with optional defaults if values cannot be found
fetcher = ValueFetcher({
    'MY_PARAM': 'Default value if none can be found',
})

# Retrieve values from supported AWS sources
my_secret = fetcher.get('MY_SECRET')
my_param = fetcher.get('MY_PARAM')

print(my_secret)
print(my_param)
```

The above scripts would be called by the following shell script:
```shell
#!/usr/bin/bash
MY_PARAM_SOURCE="aws_ssm_parameter_store"
MY_PARAM_PARAMETER_STORE_NAME="/my/parameter/store/key/name"

MY_SECRET_SOURCE="aws_secrets_manager"
MY_SECRET_SECRETS_MANAGER_NAME="my/secrets/manager/key/name"

export MY_PARAM_SOURCE MY_PARAM_PARAMETER_STORE_NAME
export MY_SECRET_SOURCE MY_SECRET_SECRETS_MANAGER_NAME

# For AWS ensure credentials are available, e.g. with AWS SSO, aws-vault, aws-profile etc.
python app.py
```

## Development
This project uses Poetry for package management.
After cloning, run:
```
./scripts/poetry.sh
```
to install dependencies for local development and running tests, etc.
### Tests

To run static code analysers and unit tests:
```
./scripts/validate.sh
```
