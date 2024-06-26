#!/usr/bin/python3


from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
import socket
import os
import time
import logging

logging.basicConfig(format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

credential = ManagedIdentityCredential()
vaultname = socket.gethostname()
vault_url  = f'https://{vaultname}.vault.azure.net/'

secrets = [
  ["privkey", "/root/.ssh/id_rsa"],
  ["privkey", "/root/privkey"],
  ["pubkey",  "/root/pubkey"],
]

client = SecretClient(vault_url=vault_url, credential=credential)
for valuepair in secrets:
    secret_name = valuepair[0]
    filename    = valuepair[1]
    logging.debug("Looking for secret %s", secret_name)
    nosecret = True
    i=0
    while nosecret and i <= 5:
        list_of_secrets = client.list_properties_of_secrets()
        secrets_names = [ secret.name for secret in list_of_secrets ]
        logging.debug("List of secrets returned by the vault %s", ' '.join(secrets_names))
        if secret_name in secrets_names:
            nosecret = False
        else:
            i = i+1
            time.sleep(20)

    logging.debug("Number of iterations had to wait to retrieve %s : %d",secret_name, i)
    if i > 5:
        logging.critical("Could not find secret %s", secret_name)
        raise Exception("Secret not found or not populated on time!")

    logging.debug("trying to get %s secret", secret_name)
    secret = client.get_secret(secret_name)
    f = open(filename,"wt")
    f.write(secret.value)
    f.close()
    os.chmod(filename,0o600)

with open("/root/ansible/ansible_vars", "w") as ha_vars:
   ha_vars.write("---\n")
   for secret_name in [ "subscriptionid", "resourcegroup", "firstnode", "machineslist", "serviceip" ]:
       logging.debug("Looking for secret %s", secret_name)
       nosecret = True
       i=0
       while nosecret and i <= 5:
           list_of_secrets = client.list_properties_of_secrets()
           secrets_names = [ secret.name for secret in list_of_secrets ]
           logging.debug("List of secrets returned by the vault %s", ' '.join(secrets_names))
           if secret_name in secrets_names:
               nosecret = False
           else:
               i = i+1
               time.sleep(20)
   
       logging.debug("Number of iterations had to wait to retrieve %s : %d",secret_name, i)
       if i > 5:
           logging.critical("Could not find secret %s", secret_name)
           raise Exception("Secret not found or not populated on time!")
   
       logging.debug("trying to get %s secret", secret_name)
       secret = client.get_secret(secret_name)
       ha_vars.write("{}: {}\n".format(secret_name,secret.value))

with open("/root/ansible/hosts", "a") as hosts:
    secret_name = "machineslist"
    logging.debug("Looking for secret %s", secret_name)
    nosecret = True
    i=0
    while nosecret and i <= 5:
        list_of_secrets = client.list_properties_of_secrets()
        secrets_names = [ secret.name for secret in list_of_secrets ]
        logging.debug("List of secrets returned by the vault %s", ' '.join(secrets_names))
        if secret_name in secrets_names:
            nosecret = False
        else:
            i = i+1
            time.sleep(20)

    logging.debug("Number of iterations had to wait to retrieve %s : %d",secret_name, i)
    if i > 5:
        logging.critical("Could not find secret %s", secret_name)
        raise Exception("Secret not found or not populated on time!")

    logging.debug("trying to get %s secret", secret_name)
    secret = client.get_secret(secret_name)
    for machine in  secret.value.split(','):
        # hosts.write(machine"\n")
        print(machine, file=hosts, sep='\n')
