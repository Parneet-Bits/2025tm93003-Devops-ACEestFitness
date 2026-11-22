
# Rolling Update Deployment

## Overview

Rolling Update is the default Kubernetes deployment strategy. It gradually replaces existing application pods with new pods while keeping the application available.

For ACEest Fitness & Gym, this strategy allows us to deploy updated application versions without stopping the entire service.

## Configuration

The deployment uses the following rolling update settings:

- **Replicas:** 2
- **Max Surge:** 1
- **Max Unavailable:** 0
- **Deployment Strategy:** RollingUpdate

These settings allow Kubernetes to create one additional pod during an update while ensuring that the desired number of available replicas is maintained.

## Deployment

Apply the rolling update deployment:

```bash
kubectl apply -f kubernetes/deployment.yml
```

Check deployment status:

```bash
kubectl get deployments -n aceest-fitness
kubectl get pods -n aceest-fitness
```

## Update Application Version

Update the container image to the required version:

```bash
kubectl set image deployment/aceest-fitness \
  aceest-fitness=YOUR_DOCKERHUB_USERNAME/aceest-fitness:2.0.0 \
  -n aceest-fitness
```

Monitor the rollout:

```bash
kubectl rollout status deployment/aceest-fitness -n aceest-fitness
```

## Rollback

If the updated version causes issues, revert to the previous deployment revision:

```bash
kubectl rollout undo deployment/aceest-fitness -n aceest-fitness
```

Check rollout history:

```bash
kubectl rollout history deployment/aceest-fitness -n aceest-fitness
```

## Verification

Verify that the application pods are running:

```bash
kubectl get pods -n aceest-fitness
kubectl get services -n aceest-fitness
```

Test the application using the Kubernetes service endpoint.

## Benefits

- Minimizes application downtime during deployments.
- Gradually replaces old pods with new pods.
- Maintains application availability during updates.
- Supports rollback to a previous deployment revision.
- Simplifies application version management.
