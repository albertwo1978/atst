# secrets-tool
secrets-tool is a group of utilities used to manage secrets in Azure environments.

*Features:*
- Generate secrets based on definitions defined in yaml
- Load secrets in to Azure KeyVault
- Wrapper for terraform to inject KeyVault secrets as environment variables

# Use Cases
## Populating KeyVault with initial secrets
In many environments, a complete list of secrets is sometimes forgotten or not well defined. With secrets-tool, all those secrets can be defined programatically and generated when creating new environments. This avoids putting in "test" values for passwords and guessible username/password combinations. Even usernames can be generated.

With both usernames and passwords generated, the application only needs to make a call out to KeyVault for the key that it needs (assuming the application, host, or vm has access to the secret)

Ex.
```
{
    'postgres_root_user': 'EzTEzSNLKQPHuJyPdPloIDCAlcibbl',
    'postgres_root_password': "2+[A@E4:C=ubb/#R#'n<p|wCW-|%q^" <!-- pragma: allowlist secret -->
}
```

## Rotating secrets
Rotating passwords is a snap! Just re-run secrets-tool and it will generate and populate new secrets.

**Be careful!! There is no safeguard to prevent you from accidentally overwriting secrets!! - To be added if desired**

## Terraform Secrets
Terraform typically expects user defined secrets to be stored in either a file, or in another service such as keyvault. The terraform wrapper feature, injects secrets from keyvault in to the environment and then runs terraform.

This provides a number of security benefits. First, secrets are not on disk. Secondly, users/operators never see the secrets fly by (passerbys or voyeurs that like to look over your shoulder when deploying to production)

## Setting up the initial ATAT database

This handles bootstrapping the ATAT database with a user, schema, and initial data.

It does the following:

- Sources the Postgres root user credentials
- Source the Postgres ATAT user password
- Runs a script inside an ATAT docker container to set up the initial database user, schema, and seed data in the database

Requirements:

- docker
- A copy of the ATAT docker image. This can be built in the repo root with: `docker build . --build-arg CSP=azure -f ./Dockerfile -t atat:latest`
- You need to know the hostname for the Postgres database. Your IP must either be whitelisted in its firewall rules or you must be behind the VPN.
- You will need a YAML file listing all the CCPO users to be added to the database, with the format:

```
- dod_id: "2323232323"
  first_name: "Luke"
  last_name: "Skywalker"
- dod_id: "5656565656"
  first_name: "Han"
  last_name: "Solo"
```

- There should be a password for the ATAT database user in the application Key Vault, preferably named `PGPASSWORD`. You can load this by running `secrets-tool --keyvault [operator key vault url] load -f postgres-user.yml` and supplying YAML like:

```
---
- PGPASSWORD:
    type: 'password'
    length: 30
```

This command takes a lot of arguments. Run `secrets-tool database --keyvault [operator key vault url] provision -- help` to see the full list of available options.

The command supplies some defaults by assuming you've followed the patterns in sample-secrets.yml and elsewhere.

An example would be:

```
secrets-tool database --keyvault [operator key vault URL] provision --app-keyvault [application key vault URL] --dbname jedidev-atat --dbhost [database host name] --ccpo-users /full/path/to/users.yml
```

# Setup

*Requirements*
- Python 3.7+
- pipenv

```
cd secrets-tool
pipenv install
pipenv shell
```

You will also need to make sure secrets-tool is in your PATH

```
echo 'PATH=$PATH:<path to secrets-tool>' > ~/.bash_profile
. ~/.bash_profile
```

`$ which secrets-tool` should show the full path

# Usage
## Defining secrets
The schema for defining secrets is very simplistic for the moment.
```yaml
---
- postgres-root-user:
    type: 'username'
    length: 30
- postgres-root-password:
    type: 'password'
    length: 30
```
In this example we're randomly generating both the username and password. `secrets-tool` is smart enough to know that a username can't have symbols in it. Passwords contain symbols, upper/lower case, and numbers. This could be made more flexible and configurable in the future.


## Populating secrets from secrets definition file
This process is as simple as specifying the keyvault and the definitions file.
```
secrets-tool secrets --keyvault https://operator-dev-keyvault.vault.azure.net/ load -f ./sample-secrets.yaml
```

## Running terraform with KeyVault secrets
This will fetch all secrets from the keyvault specified. `secrets-tool` then converts the keys to a variable name that terraform will look for. Essentially it prepends the keys found in KeyVault with `TF_VAR` and then executes terraform as a subprocess with the injected environment variables.
```
secrets-tool terraform --keyvault https://operator-dev-keyvault.vault.azure.net/ plan
```
