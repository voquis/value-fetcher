"""
Base using AWS Secrets Manager unit tests
"""

import os

import pytest
from moto import mock_secretsmanager
from tests import utils
from value_fetcher import ValueFetcher

# Set mocked boto (moto) client default values
os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

fetcher = ValueFetcher()

@mock_secretsmanager
def test_aws_secrets_manager_success(monkeypatch):
    """
    Test fetching config values from secrets manager
    """

    # Instruct config provider to fetch value for SM_TEST from secrets manager
    monkeypatch.setenv('SECRET_OK_SOURCE', 'aws_secrets_manager')

    # Create mocked test parameter to later fetch using moto
    utils.put_secretsmanager_secret('/is/ok', 'my secret')

    # Assert value is correctly retrieved if the key name is provided
    monkeypatch.setenv('SECRET_OK_SECRETS_MANAGER_NAME', '/is/ok')
    assert fetcher.get('SECRET_OK') == 'my secret'


@mock_secretsmanager
def test_aws_secrets_manager_no_name(monkeypatch):
    """
    Test fetching config values from secrets manager without specifying a name
    """

    monkeypatch.setenv('SECRET_NONAME_SOURCE', 'aws_secrets_manager')

    with pytest.raises(ValueError) as exception:
        fetcher.get('SECRET_NONAME')

    msg = 'Missing or empty environment value for SECRET_NONAME_SECRETS_MANAGER_NAME'
    assert str(exception.value) == msg


@mock_secretsmanager
def test_aws_secrets_manager_does_not_exist(monkeypatch):
    """
    Test fetching non-existent config values from secrets manager
    """

    monkeypatch.setenv('SECRET_NONEXISTENT_SOURCE', 'aws_secrets_manager')
    monkeypatch.setenv('SECRET_NONEXISTENT_SECRETS_MANAGER_NAME', '/does/not/exist')
    # Assert an exception is thrown if secret name is not provided
    with pytest.raises(ValueError) as exception:
        fetcher.get('SECRET_NONEXISTENT')

    msg = 'Missing or empty AWS Secrets Manager value for /does/not/exist'
    assert str(exception.value) == msg
