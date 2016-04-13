# Configuration file for Jupyter Hub

import os
import sys

c = get_config()

c.JupyterHub.log_level = 10
c.JupyterHub.spawner_class = 'dockerspawner.SystemUserSpawner'
c.DockerSpawner.container_image = 'jupyter/scipy-singleuser'
c.DockerSpawner.use_internal_ip = True

c.SystemUserSpawner.host_homedir_format_string = '/data/shared/{username}'

import socket
ips = ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1])
c.JupyterHub.hub_ip = ips[0]


c.JupyterHub.authenticator_class = 'oauthenticator.LocalGitHubOAuthenticator'
c.LocalGitHubOAuthenticator.create_system_users = True

c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()

join = os.path.join

here = os.path.dirname(__file__)
root = os.environ.get('OAUTHENTICATOR_DIR', here)
sys.path.insert(0, root)

with open(join(root, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)

c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# ssl config
ssl = join(root, 'ssl')
keyfile = join(ssl, 'ssl.key')
certfile = join(ssl, 'ssl.cert')
if os.path.exists(keyfile):
    c.JupyterHub.ssl_key = keyfile
if os.path.exists(certfile):
    c.JupyterHub.ssl_cert = certfile
