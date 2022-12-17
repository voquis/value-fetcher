"""
Pytest unit tests for aws client calls
"""

import os
from moto import mock_ssm, mock_secretsmanager
from value_fetcher.aws import Aws
from tests import utils

# Set boto client default values
os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

@mock_ssm
def test_getting_parameter():
    """
    Check an SSM parameter is returned
    """

    # Create test parameter to later fetch using moto
    utils.ssm_put_parameter_securestring()

    # Fetch and verify parameter
    aws = Aws()
    param = aws.get_parameter_value('test')
    assert param == 'abc'

    # Assert missing parameter returns nothing
    assert not aws.get_parameter_value('doesnotexist')


@mock_secretsmanager
def test_getting_secret():
    """
    Check string and binary secrets may be retrieved
    """

    # Create mocked secrets to later fetch using moto
    secret_string = 'my secret value'
    secret_binary = bytes(secret_string, 'utf-8')
    utils.put_secretsmanager_secret('/secret/string', secret_string)
    utils.put_secretsmanager_secret('/secret/binary', None, secret_binary)

    # Fetch secrets
    aws = Aws()
    assert aws.get_secret_value('/secret/string') == secret_string
    assert aws.get_secret_value('/secret/binary') == secret_string
    assert not aws.get_secret_value('/does/not/exist')
