# Run the web-app in a Kubernetes cluster

## Setup the local development K8S cluster (with `kind`)

### Start the K8S cluster

```shell
./create-k8s-kind-cluster.sh

# Check that the cluster is up and running:
kubectl cluster-info

# To delete this kind cluster:
kind delete cluster
```

### Push your docker images inside the K8S cluster

```shell
# Will build the docker image locally and then will push the docker image into the kind cluster
./build-and-push-image-to-kind.sh
```

## Deploy the web-app into a K8S cluster

The web-app is composed of 2 service:

* `backend`: a python backend that stores data and process it
* `frontend`: a `nginx` server that renders the React app that is displayed to the end-user

To deploy this, we are creating a `deployment` (a group of `pods` that is managed by K8S) and 
a `service` (a set of policy describing how to access defined `pods`).
The file `web-app.yml` contains the definition of both `deployment` and `service`.

To add these into the kubernetes state, one need to apply this file with `kubectl apply -f web-app.yml`.

One can also simply run this script:
```shell
./deploy-to-k8s.sh
```
