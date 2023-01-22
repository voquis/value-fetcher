"""
Provider unit tests
"""

import os

import pytest
from value_fetcher import ValueFetcher

# Set mocked boto (moto) client default values
os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

fetcher = ValueFetcher()

def test_invalid_names():
    """
    Assert invalid or empty names produce exceptions
    """
    # Test non-existent variable throws an exception
    with pytest.raises(ValueError) as exception:
        fetcher.get('')

    with pytest.raises(ValueError) as env_exception:
        fetcher.get_from_env('')

    with pytest.raises(ValueError) as ps_exception:
        fetcher.get_from_aws_ssm_parameter_store('')

    with pytest.raises(ValueError) as sm_exception:
        fetcher.get_from_aws_secrets_manager('')

    assert str(exception.value) == 'Invalid key name provided'
    assert str(env_exception.value) == 'Missing or empty environment key'
    assert str(ps_exception.value) == 'Missing or empty environment value for _PARAMETER_STORE_NAME'
    assert str(sm_exception.value) == 'Missing or empty environment value for _SECRETS_MANAGER_NAME'


def test_unknown_source(monkeypatch):
    """
    Test unknown source raises an exception
    """
    monkeypatch.setenv('UNKNOWN', 'test_value')
    monkeypatch.setenv('UNKNOWN_SOURCE', 'unknown')
    # Test unknown source returns nothing
    with pytest.raises(ValueError) as exception:
        fetcher.get('UNKNOWN')

    assert 'Unknown source' in str(exception.value)
