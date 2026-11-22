
# Canary Deployment

## Overview

Canary Deployment is a deployment strategy in which a new application version is released to a small percentage of users while the majority continue using the stable version.

For ACEest Fitness & Gym, this strategy allows us to test a new application version with limited traffic before making it available to everyone.

This implementation uses Kubernetes Deployments, Services, and Istio VirtualService for traffic distribution.

## Configuration

The deployment uses the following Kubernetes resources:

| File | Purpose |
|---|---|
| `blue-deployment.yml` | Runs the stable application version |
| `green-deployment.yml` | Runs the new canary application version |
| `canary-service.yml` | Creates stable and canary Services |
| `canary-routing.yml` | Configures traffic distribution using Istio |

## Step 1: Deploy Stable Version

Apply the stable deployment:

```bash
kubectl apply -f kubernetes/blue-deployment.yml
```

Verify the stable pods:

```bash
kubectl get pods -n aceest-fitness -l version=blue
```

## Step 2: Deploy Canary Version

Apply the canary deployment:

```bash
kubectl apply -f kubernetes/green-deployment.yml
```

Verify the canary pods:

```bash
kubectl get pods -n aceest-fitness -l version=green
```

Wait for the canary deployment to become ready:

```bash
kubectl rollout status deployment/aceest-fitness-green -n aceest-fitness
```

## Step 3: Create Stable and Canary Services

Apply the Services:

```bash
kubectl apply -f kubernetes/canary-service.yml
```

The stable Service selects pods with `version: blue`, while the canary Service selects pods with `version: green`.

## Step 4: Configure Traffic Distribution

Apply the Istio Gateway and canary routing configuration:

```bash
kubectl apply -f kubernetes/istio-gateway.yml
kubectl apply -f kubernetes/canary-routing.yml
```

The traffic distribution is configured as:

- **90%** of requests go to the stable version.
- **10%** of requests go to the canary version.

## Step 5: Verify Traffic Routing

Check the Istio VirtualService:

```bash
kubectl get virtualservice aceest-fitness-canary -n aceest-fitness
```

Check the Services:

```bash
kubectl get services -n aceest-fitness
```

Check the deployments and pods:

```bash
kubectl get deployments -n aceest-fitness
kubectl get pods -n aceest-fitness
```

## Step 6: Promote or Roll Back

If the canary version performs successfully, update the routing weights to send 100% of traffic to the canary version.

If errors or performance issues occur, update the routing weights to send 100% of traffic to the stable version.

After editing the routing configuration, apply it again:

```bash
kubectl apply -f kubernetes/canary-routing.yml
```

## Benefits

- Limits the impact of a new release.
- Allows testing with real application traffic.
- Supports gradual application releases.
- Helps identify issues before full deployment.
- Provides a straightforward rollback by changing traffic weights.

## Prerequisites

- Kubernetes cluster
- Istio installed in the cluster
- Istio ingress gateway available
- Stable and canary deployments running
- Stable and canary Services configured
