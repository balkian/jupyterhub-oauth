# Configuration file for Jupyter Hub

import os
import sys
import json
import grp
from os.path import join

c = get_config()

PREADMINS = set(os.environ.get('ADMINS', '').split(','))
OAUTH_CLASS = os.environ.get('OAUTH_CLASS', 'oauthenticator.GitHub')
HOME_FORMAT_STRING = os.environ.get('HOST_HOMEDIR', '/mnt/home/{username}')
here = os.path.dirname(__file__)
root = os.environ.get('OAUTHENTICATOR_DIR', here)
udir = os.environ.get('USERS_DIR', root)
sys.path.insert(0, root)
teams = os.environ.get('OAUTHENTICATOR_TEAMS', None)

c.JupyterHub.log_level = 10
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.container_image = 'jupyter/scipy-notebook'
c.DockerSpawner.use_internal_ip = True

notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { HOME_FORMAT_STRING: notebook_dir }

common = os.environ.get('COMMON_DIR')

if common:
    c.DockerSpawner.volumes[common] = join(notebook_dir, 'common')

dsdir = os.environ.get('DATASETS_DIR')

if dsdir:
    c.DockerSpawner.read_only_volumes = { dsdir: join(notebook_dir, 'DATASETS')}

import socket
ips = ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1])
c.JupyterHub.hub_ip = ips[0]

# c.JupyterHub.authenticator_class = 'oauthenticator.{}'.format(auth_class_name)
c.JupyterHub.authenticator_class = OAUTH_CLASS
# auth_class = getattr(c, 'auth_class_name')
# auth_class = getattr(c, 'GitHubOAuthenticator')
# auth_class.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
# auth_class = getattr(c, auth_short_name)
# auth_class.create_system_users = False

c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = PREADMINS
# ssl config
ssl = join(root, 'ssl')
keyfile = join(ssl, 'ssl.key')
certfile = join(ssl, 'ssl.cert')
if os.path.exists(keyfile):
    c.JupyterHub.ssl_key = keyfile
if os.path.exists(certfile):
    c.JupyterHub.ssl_cert = certfile

# load_from_json()
