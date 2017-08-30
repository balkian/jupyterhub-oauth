VERSION=`cat VERSION`
REPO="gsiupm/jupyterhub-oauth"
TEST=$(REPO):test-$(VERSION)
FINAL=$(REPO):$(VERSION)


Dockerfile: Dockerfile.template VERSION
	cat Dockerfile.template | VERSION=$(VERSION) envsubst > Dockerfile

build: Dockerfile
	docker build -t $(TEST) .

run:
	docker run -v $$PWD/output:/output -p 8000:8000 -v /var/run/docker.sock:/var/run/docker.sock -v $(PWD)/jupyterhub_config.py:/srv/jupyterhub/jupyterhub_config.py --env-file .env $(TEST) jupyterhub --config /srv/jupyterhub/jupyterhub_config.py --no-ssl

push:

.PHONY: build run

push: build
	docker tag $(TEST) $(FINAL)
	docker tag $(TEST) $(REPO)
	docker rmi $(TEST)
	docker push $(FINAL)
	docker push $(REPO)

.PHONY: build run push
