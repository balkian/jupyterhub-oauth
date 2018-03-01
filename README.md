# OAuthenticator

Example of running [JupyterHub](https://github.com/jupyter/jupyterhub)
with [GitHub OAuth](https://developer.github.com/v3/oauth/) for authentication.

By default, this image uses `oauthenticator.GitHub`, but you can use a different class by setting `OAUTH_CLASS` in your environment.
Other configuration parameters, including specific values for your oauth class, can be configured via environment variables.
For convenience, we include instructions for GITLAB and GITHUB below.

This image uses `DockerSpawner` to launch user servers.
The result is that each user gets their own isolated container in the server, using the docker image specified in the config.
For other options (e.g. Kubernetes or local), check out: https://github.com/jupyterhub/jupyterhub#spawners

## Variables


### General variables

```
ADMINS=balkian,oaraque
OAUTH_CALLBACK_URL=http://hub.cluster.gsi.dit.upm.es/hub/oauth_callback
HOST_HOMEDIR=/mnt/home/{username} # {username} will be replaced by the actual OAuth user
```

### Git lab variables:

```
GITLAB_HOST=https://lab.cluster.gsi.dit.upm.es/
GITLAB_CLIENT_ID=TheMaxiID
GITLAB_CLIENT_SECRET=TheMaxiSecret
OAUTH_CLASS=oauthenticator.gitlab.GitLabOAuthenticator 
DATASETS_DIR=/home/datasets # READ ONLY
COMMON_DIR=/home/common # To share files between users
```

### GitHub variables:

```
GITHUB_CLIENT_ID=GHId
GITHUB_CLIENT_SECRET=GHSecret
OAUTH_CLASS=oauthenticator.github.GitHubOAuthenticator 
```


## Docker-compose

This repository includes a docker-compose file to automate building and running the image.
To use it, save your environment variables to `.env`.

Then, just build the image and run an instance with a single command:


```
docker-compose run --build
```


## Docker-swarm

DockerSpawner works with the old docker-swarm standalone mode, just by mounting your swarm socket to `/var/run/docker.sock`. e.g.:

```
-v "/var/run/swarm.sock:/var/run/docker.sock"
```

If you are using the new swarm mode in docker, you might want to check out this issue: https://github.com/jupyterhub/dockerspawner/issues/215


## Manual instructions
### Build

Build the container with:

    make build
    
Alternatively:

    docker build -t gsiupm/jupyter-oauth:testing .

### Run

Add your oauth client id, client secret, and callback URL to your `env file` (i.e. `.env`).
Once you have built the container, you can run it with:

    make run
    
Alternatively:

    docker run -it -p 8000:8000 --env-file=env gsiupm/jupyter-oauth:testing

Which will run the Jupyter server.


### SSL

To run the server on HTTPS, put your ssl key and cert in ssl/ssl.key and
ssl/ssl.cert.


## Useful tweaks

You can add resource limits, e.g.:

```
c.Spawner.mem_limit = '10G'
```

## Known issues

If you recreate the jupyterhub image, the token for the jupyterhub server will change, and it may have trouble connecting to user containers.
We've tried setting the token manually in the config, but it did not work.

As a workaround, you could remove the containers and access them again:

```
docker ps -a | grep 'jupyter-' | cut -d' ' -f1 | xargs docker rm
```

Unfortunately, **all unsaved work will be lost**
