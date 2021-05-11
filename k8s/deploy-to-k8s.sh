#!/bin/bash

echo "Creating a K8S deployement and Service"
kubectl apply -f web-app.yml

echo "To delete, run 'kubectl delete -f web-app.yml'"
