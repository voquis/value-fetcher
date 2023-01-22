"""
Base using environment variables unit tests
"""

import pytest
from value_fetcher import ValueFetcher

fetcher = ValueFetcher()

def test_env_vars(monkeypatch):
    """
    Test fetching config values from environment
    """

    # Test fetches from environment by default
    monkeypatch.setenv('ENV_VAR_TEST', 'test_value')
    assert fetcher.get('ENV_VAR_TEST') == 'test_value'

    # Test non-existent variable throws an exception
    with pytest.raises(ValueError) as exception:
        fetcher.get('NONEXISTENT_ENV_VAR')

    assert 'Missing or empty environment value' in str(exception.value)


def test_env_vars_with_defaults():
    """
    Test fetching environment variables with defaults set
    """

    fetcher_with_defaults = ValueFetcher({
        'SET_WITH_DEFAULT': 'some_default_value'
    })

    assert fetcher_with_defaults.get('SET_WITH_DEFAULT') == 'some_default_value'
