"""
Base using AWS Secrets Manager unit tests
"""

import os

import pytest
from moto import mock_aws
from tests import utils
from value_fetcher import ValueFetcher

# Set mocked boto (moto) client default values
os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

fetcher = ValueFetcher()


@mock_aws
def test_aws_secrets_manager_called_direct_no_key_raises_error():
    """
    Test fetching from secrets manager without specifying a key raises
    exception
    """

    # Assert an exception is thrown if parameter key is not provided
    with pytest.raises(ValueError) as exception:
        fetcher.get_from_aws_secrets_manager(None)

    assert "Missing or empty AWS Secrets Manager key" in str(exception.value)

    # Assert an exception is thrown if parameter key is empty
    with pytest.raises(ValueError) as exception:
        fetcher.get_from_aws_secrets_manager("")

    assert "Missing or empty AWS Secrets Manager key" in str(exception.value)


@mock_aws
def test_aws_secrets_manager_with_env_var_config_success(monkeypatch):
    """
    Test fetching config values from secrets manager
    """

    # Instruct config provider to fetch value for SM_TEST from secrets manager
    monkeypatch.setenv("SECRET_OK_SOURCE", "aws_secrets_manager")

    # Create mocked test parameter to later fetch using moto
    utils.put_secretsmanager_secret("/is/ok", "my secret")

    # Assert value is correctly retrieved if the key name is provided
    monkeypatch.setenv("SECRET_OK_SECRETS_MANAGER_NAME", "/is/ok")
    assert fetcher.get("SECRET_OK") == "my secret"


@mock_aws
def test_aws_secrets_manager_without_env_var_config_success():
    """
    Test fetching config values from secrets manager without specifying a name
    """

    key = "/is/ok/no/env/vars"
    value = "my secret val no env var"

    # Create mocked test parameter to later fetch using moto
    utils.put_secretsmanager_secret(key, value)

    assert fetcher.get_from_aws_secrets_manager(key) == value


@mock_aws
def test_aws_secrets_manager_does_not_exist(monkeypatch):
    """
    Test fetching non-existent config values from secrets manager
    """

    key = "SECRET_NONEXISTENT_SOURCE"
    monkeypatch.setenv(key, "aws_secrets_manager")

    key = "SECRET_NONEXISTENT_SECRETS_MANAGER_NAME"
    monkeypatch.setenv(key, "/does/not/exist")

    # Assert an exception is thrown if secret name is not provided
    with pytest.raises(ValueError) as exception:
        fetcher.get("SECRET_NONEXISTENT")

    msg = "Missing or empty AWS Secrets Manager value for /does/not/exist"
    assert str(exception.value) == msg
