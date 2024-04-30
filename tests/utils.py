"""
AWS test utils
"""

import boto3


def ssm_put_parameter_securestring(name="test", value="abc"):
    """
    Create mocked SSM parameter to later fetch using moto
    """
    ssm = boto3.client("ssm")
    ssm.put_parameter(
        Name=name,
        Value=value,
        Type="SecureString",
    )


def put_secretsmanager_secret(name="test", value=None, binary=None):
    """
    Create mocked Secrets Manager secret to later fetch using moto
    """
    ssm = boto3.client("secretsmanager")
    if value is not None:
        ssm.create_secret(Name=name, SecretString=value)

    if binary is not None:
        ssm.create_secret(Name=name, SecretBinary=binary)
