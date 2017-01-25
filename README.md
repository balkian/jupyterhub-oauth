# OAuthenticator

Example of running [JupyterHub](https://github.com/jupyter/jupyterhub)
with [GitHub OAuth](https://developer.github.com/v3/oauth/) for authentication.

## Variables


### General variables

```
ADMINS=balkian,oaraque
OAUTH_CALLBACK_URL=http://hub.cluster.gsi.dit.upm.es/hub/oauth_callback
HOST_HOMEDIR=/mnt/home/{username} # {username} will be replaced by the actual OAuth user
```

## Gitlab variables:

```
GITLAB_HOST=https://lab.cluster.gsi.dit.upm.es/
GITLAB_CLIENT_ID=TheMaxiID
GITLAB_CLIENT_SECRET=TheMaxiSecret
OAUTH_CLASS=oauthenticator.gitlab.GitLabOAuthenticator 
DATASETS_DIR=/home/datasets # READ ONLY
COMMON_DIR=/home/common # To share files between users
```

## GitHub variables:

```
GITHUB_CLIENT_ID=GHId
GITHUB_CLIENT_SECRET=GHSecret
OAUTH_CLASS=oauthenticator.github.GitHubOAuthenticator 
```

## build

Build the container with:

    make build
    
Alternatively:

    docker build -t gsiupm/jupyter-oauth:testing .

### ssl

To run the server on HTTPS, put your ssl key and cert in ssl/ssl.key and
ssl/ssl.cert.

## run

Add your oauth client id, client secret, and callback URL to your `env file` (i.e. `.env`).
Once you have built the container, you can run it with:

    make run
    
Alternatively:

    docker run -it -p 8000:8000 --env-file=env gsiupm/jupyter-oauth:testing

Which will run the Jupyter server.
