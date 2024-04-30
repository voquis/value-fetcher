"""
Configuration provider to fetch values from the following sources:
- Environment variable
- AWS Systems Manager (SSM) Parameter Store
- AWS Secrets Manager
"""

import os
import logging
from .aws import Aws


class ValueFetcher:
    """
    Configuration provider class
    """

    def __init__(self, env_defaults: dict = None) -> None:
        self.env_defaults = env_defaults

    def get(self, key: str) -> str:
        """
        Given a key name MY_VAL, check for a source env var e.g. MY_VAL_SOURCE.
        Raises exception if source does not match list of known services.
        """
        # Make the provided name all-uppercase
        key = key.upper()

        if not isinstance(key, str) or len(key) == 0:
            message = "Invalid key name provided"
            logging.critical(message)
            logging.critical(key)
            raise ValueError(message)

        logging.debug("Retrieving value for key %s", key)
        source = os.environ.get(f"{key}_SOURCE", "env").lower()
        logging.debug("%s source: %s", key, source)
        # Get value from environment variable
        if source == "env":
            return self.get_from_env(key)

        # Get value from AWS SSM parameter store
        if source == "aws_ssm_parameter_store":
            return self.get_from_aws_ssm_parameter_store(key)

        # Get value from AWS Secrets Manager
        if source == "aws_secrets_manager":
            return self.get_from_aws_secrets_manager(key)

        message = f"Unknown source {source}"
        logging.critical(message)
        raise ValueError(message)

    def get_from_env(self, key) -> str:
        """
        Fetch a value from environment variables, using a default if available.
        If value is empty and cannot be found in defaults, raise exception.
        """

        if not isinstance(key, str) or len(key) == 0:
            message = "Missing or empty environment key"
            logging.critical(message)
            logging.critical(key)
            raise ValueError(message)

        logging.debug("Checking environment for key: %s", key)
        value = os.environ.get(key, "").strip()
        if not isinstance(value, str) or len(value) == 0:
            defaults = self.env_defaults
            if isinstance(defaults, dict) and key in defaults:
                logging.debug("Using default value for env var: %s", key)
                value = defaults[key]
            else:
                message = f"Missing or empty environment value for {key}"
                logging.critical(message)
                raise ValueError(message)

        return value

    def get_from_aws_ssm_parameter_store(self, key: str) -> str:
        """
        Fetch a value from AWS SSM Parameter store.
        If the parameter name is not configured by an environment variable,
        try the provided key.
        """

        if not isinstance(key, str) or len(key) == 0:
            message = "Missing or empty AWS SSM Parameter Store key"
            logging.critical(message)
            raise ValueError(message)

        name_key = f"{key}_PARAMETER_STORE_NAME"

        logging.debug("Checking env for AWS SSM Parameter %s", name_key)
        try:
            name = self.get_from_env(name_key)
            logging.debug("Using parameter name %s", name)
        except ValueError as exception:
            logging.debug(exception)
            logging.debug("Using key name for parameter %s", key)
            name = key

        aws = Aws()
        value = aws.get_parameter_value(name)
        if not isinstance(value, str) or len(value) == 0:
            message = f"Missing or empty AWS SSM Parameter Store {name}"
            logging.critical(message)
            raise ValueError(message)

        return value

    def get_from_aws_secrets_manager(self, key: str) -> str:
        """
        Fetch a value from AWS Secrets Manager.
        If the secret name is not configured by an environment variable,
        use the key directly.
        """

        if not isinstance(key, str) or len(key) == 0:
            message = "Missing or empty AWS Secrets Manager key"
            logging.critical(message)
            raise ValueError(message)

        name_key = f"{key}_SECRETS_MANAGER_NAME"

        logging.debug("Checking env for AWS Secret Manager %s", name_key)
        try:
            name = self.get_from_env(name_key)
            logging.debug("Using secret name %s", name)
        except ValueError as exception:
            logging.debug(exception)
            logging.debug("Using key name for secret %s", key)
            name = key

        aws = Aws()
        value = aws.get_secret_value(name)
        if not isinstance(value, str) or len(value) == 0:
            message = f"Missing or empty AWS Secrets Manager value for {name}"
            logging.critical(message)
            raise ValueError(message)

        return value
