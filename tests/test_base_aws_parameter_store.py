"""
Base using AWS Systems Manager Parameter Store unit tests
"""

import os

import pytest
from moto import mock_ssm
from tests import utils
from value_fetcher import ValueFetcher

# Set mocked boto (moto) client default values
os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

fetcher = ValueFetcher()

@mock_ssm
def test_aws_ssm_parameter_store_success(monkeypatch):
    """
    Test fetching config values from parameter store
    """

    # Instruct config provider to fetch value for SSM_TEST from parameter store
    monkeypatch.setenv('SSM_OK_SOURCE', 'aws_ssm_parameter_store')

    # Create mocked test parameter to later fetch using moto
    utils.ssm_put_parameter_securestring('/is/ok', 'my val')

    # Assert value is correctly retrieved if the key name is provided
    monkeypatch.setenv('SSM_OK_PARAMETER_STORE_NAME', '/is/ok')
    assert fetcher.get('SSM_OK') == 'my val'


@mock_ssm
def test_aws_ssm_parameter_store_no_name(monkeypatch):
    """
    Test fetching config values from parameter store without specifying a name
    """

    monkeypatch.setenv('SSM_NONAME_SOURCE', 'aws_ssm_parameter_store')

    with pytest.raises(ValueError) as exception:
        fetcher.get('SSM_NONAME')

    msg = 'Missing or empty environment value for SSM_NONAME_PARAMETER_STORE_NAME'
    assert str(exception.value) == msg


@mock_ssm
def test_aws_ssm_parameter_store_does_not_exist(monkeypatch):
    """
    Test fetching non-existent config values from parameter store
    """

    monkeypatch.setenv('SSM_NONEXISTENT_SOURCE', 'aws_ssm_parameter_store')
    monkeypatch.setenv('SSM_NONEXISTENT_PARAMETER_STORE_NAME', '/does/not/exist')
    # Assert an exception is thrown if parameter name is not provided
    with pytest.raises(ValueError) as exception:
        fetcher.get('SSM_NONEXISTENT')

    assert 'Missing or empty AWS SSM Parameter Store value ' in str(exception.value)
