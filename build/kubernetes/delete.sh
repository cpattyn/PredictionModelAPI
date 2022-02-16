#!/bin/bash

kubectl delete ingress project2-ingress
kubectl delete service project2-service
kubectl delete deployment project2-deployment

