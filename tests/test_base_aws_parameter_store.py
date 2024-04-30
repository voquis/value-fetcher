"""
Base using AWS Systems Manager Parameter Store unit tests
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
def test_aws_ssm_parameter_store_called_direct_no_key_raises_error():
    """
    Test fetching from parameter store without specifying a key raises
    exception
    """

    # Assert an exception is thrown if parameter key is not provided
    with pytest.raises(ValueError) as exception:
        fetcher.get_from_aws_ssm_parameter_store(None)

    val = exception.value
    assert "Missing or empty AWS SSM Parameter Store key" in str(val)

    # Assert an exception is thrown if parameter key is empty
    with pytest.raises(ValueError) as exception:
        fetcher.get_from_aws_ssm_parameter_store("")

    val = exception.value
    assert "Missing or empty AWS SSM Parameter Store key" in str(val)


@mock_aws
def test_aws_ssm_parameter_store_with_env_var_config_success(monkeypatch):
    """
    Test fetching config values from parameter store with key name from
    environment
    """

    # Instruct config provider to fetch value for SSM_TEST from parameter store
    monkeypatch.setenv("SSM_OK_SOURCE", "aws_ssm_parameter_store")

    # Create mocked test parameter to later fetch using moto
    utils.ssm_put_parameter_securestring("/is/ok", "my val")

    # Assert value is correctly retrieved if the key name is provided
    monkeypatch.setenv("SSM_OK_PARAMETER_STORE_NAME", "/is/ok")
    assert fetcher.get("SSM_OK") == "my val"


@mock_aws
def test_aws_ssm_parameter_store_without_env_var_config_success():
    """
    Test fetching config values from parameter store with no additional
    environment variables.
    """

    key = "/is/ok/no/env/vars"
    value = "my val no env var"

    # Create mocked test parameter to later fetch using moto
    utils.ssm_put_parameter_securestring(key, value)

    assert fetcher.get_from_aws_ssm_parameter_store(key) == value


@mock_aws
def test_aws_ssm_parameter_store_does_not_exist(monkeypatch):
    """
    Test fetching non-existent config values from parameter store
    """
    key = "SSM_NONEXISTENT_SOURCE"
    monkeypatch.setenv(key, "aws_ssm_parameter_store")

    key = "SSM_NONEXISTENT_PARAMETER_STORE_NAME"
    monkeypatch.setenv(key, "/does/not/exist")

    # Assert an exception is thrown if parameter name is not provided
    with pytest.raises(ValueError) as exception:
        fetcher.get("SSM_NONEXISTENT")

    assert "Missing or empty AWS SSM Parameter Store" in str(exception.value)
