import logging
import yaml
import secrets
import string
from pathlib import Path
from .auth import Auth
from azure.keyvault.secrets import SecretClient

logger = logging.getLogger(__name__)

class SecretsClient(Auth):
    def __init__(self, *args, **kwargs):
        super(SecretsClient, self).__init__(*args, **kwargs)
        self.secret_client = SecretClient(vault_url=self.vault_url, credential=self.credentials)

    def get_secret(self, key):
        secret = self.secret_client.get_secret(key)
        return secret.value

    def set_secret(self, key: str, value: str):
        secret = self.secret_client.set_secret(key, value)
        logger.debug('Set value for key: {}'.format(key))
        return secret

    def list_secrets(self):
        secrets = list()
        secret_properties = self.secret_client.list_properties_of_secrets()
        for secret in secret_properties:
            secrets.append(secret.name)
        return secrets

class SecretsLoader():
    """
    Helper class to load secrets definition, generate
    the secrets a defined by the defintion, and then
    load the secrets in to keyvault
    """
    def __init__(self, yaml_file: str, keyvault: object):
        assert Path(yaml_file).exists()
        self.yaml_file = yaml_file
        self.keyvault = keyvault
        self.config = dict()

        self._load_yaml()
        self._generate_secrets()

    def _load_yaml(self):
        with open(self.yaml_file) as handle:
            self.config = yaml.load(handle, Loader=yaml.FullLoader)

    def _generate_secrets(self):
        secrets = GenerateSecrets(self.config).process_definition()
        self.secrets = secrets

    def load_secrets(self):
        for key, val in self.secrets.items():
            print('{} {}'.format(key,val))
            self.keyvault.set_secret(key=key, value=val)


class GenerateSecrets():
    """
    Read the secrets definition and generate requiesite
    secrets based on the type of secret and arguments
    provided
    """
    def __init__(self, definitions: dict):
        self.definitions = definitions
        most_punctuation = string.punctuation.replace("'", "").replace('"', "")
        self.password_characters = string.ascii_letters + string.digits + most_punctuation

    def process_definition(self):
        """
        Processes a simple definiton such as the following
        ```
        - postgres_root_user:
            type: 'username'
            length: 30
        - postgres_root_password:
            type: 'password'
            length: 30
        ```
        This should be broken out to a function per definition type
        if the scope extends in to tokens, salts, or other specialized
        definitions.
        """
        try:
            secrets = dict()
            for definition in self.definitions:
                key = list(definition)
                def_name = key[0]
                secret = definition[key[0]]
                assert len(str(secret['length'])) > 0
                method = getattr(self, '_generate_'+secret['type'])
                value = method(secret['length'])
                #print('{}: {}'.format(key[0], value))
                secrets.update({def_name: value})
            logger.debug('Setting secrets to: {}'.format(secrets))
            return secrets
        except KeyError as e:
            logger.error('Missing the {} key in the definition'.format(e))

    # Types. Can be usernames, passwords, or in the future things like salted
    # tokens, uuid, or other specialized types
    def _generate_password(self, length: int):
        return ''.join(secrets.choice(self.password_characters) for i in range(length))

    def _generate_username(self, length: int):
        self.username_characters = string.ascii_letters
        return ''.join(secrets.choice(self.username_characters) for i in range(length))
