"""
Interact with the following AWS services to fetch values:
  - SSM Parameter store to fetch encrypted parameters
  - Secrets Manager to fetch secret values
"""

import logging
import boto3
import botocore


class Aws:
    """
    Fetch parameters and send emails.
    """

    def __init__(self) -> None:
        # Prepare AWS clients
        self.ssm = boto3.client("ssm")
        self.secretsmanager = boto3.client("secretsmanager")

    def get_parameter_value(self, name) -> str:
        """
        Fetch encrypted parameters from Systems Manager (SSM) Parameter Store
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html
        """

        value = None

        logging.debug("Fetching AWS SSM Parameter Store parameter: %s", name)
        try:
            response = self.ssm.get_parameter(Name=name, WithDecryption=True)
            if "Parameter" in response:
                if "Value" in response["Parameter"]:
                    value = response["Parameter"]["Value"]
        except (
            botocore.exceptions.ClientError,
            botocore.exceptions.NoCredentialsError,
            self.ssm.exceptions.InternalServerError,
            self.ssm.exceptions.InvalidKeyId,
            self.ssm.exceptions.ParameterNotFound,
            self.ssm.exceptions.ParameterVersionNotFound,
        ) as exception:
            logging.warning("AWS SSM Parameter fetch failed: %s", name)
            logging.warning(exception)

        return value

    def get_secret_value(self, name) -> str:
        """
        Fetch encrypted secret from Secrets Manager
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html
        """

        value = None
        logging.debug("Fetching AWS Secrets Manager secret: %s", name)

        try:
            response = self.secretsmanager.get_secret_value(SecretId=name)
            if "SecretString" in response:
                value = response["SecretString"]
            elif "SecretBinary" in response:
                value = response["SecretBinary"]
                if isinstance(value, bytes):
                    value = value.decode("utf-8")
        except (
            botocore.exceptions.ClientError,
            botocore.exceptions.NoCredentialsError,
            self.secretsmanager.exceptions.ResourceNotFoundException,
            self.secretsmanager.exceptions.InvalidParameterException,
            self.secretsmanager.exceptions.InvalidRequestException,
            self.secretsmanager.exceptions.DecryptionFailure,
            self.secretsmanager.exceptions.InternalServiceError,
        ) as exception:
            logging.warning("AWS Secrets Manager fetch failed: %s", name)
            logging.warning(exception)

        return value
