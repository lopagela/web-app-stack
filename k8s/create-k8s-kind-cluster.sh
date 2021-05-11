#!/bin/bash

# kind is an easy way to create small local kubernetes cluster.
# This is used for local development only and it should not be used in production

echo "Creating a cluster with kind"
kind create cluster --config kind-config.yml

echo "Cluster created, now adding the nginx ingress-controller"
# Source: https://kubernetes.github.io/ingress-nginx/deploy/
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.46.0/deploy/static/provider/cloud/deploy.yaml
kubectl get pods -n ingress-nginx

echo "Cluster created, you can remove it with 'kind delete cluster'"
