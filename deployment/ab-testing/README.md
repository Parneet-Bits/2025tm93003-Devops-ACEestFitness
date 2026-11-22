
# A/B Testing Deployment

## Overview

A/B Testing is a deployment strategy in which incoming application traffic is divided between two different application versions to compare their behavior and performance.

For ACEest Fitness & Gym, this strategy allows us to test two versions of the application with different user groups and evaluate which version provides better results.

This implementation uses Kubernetes Deployments, Services, and Istio VirtualService for header-based traffic routing.

## Configuration

The deployment uses the following Kubernetes resources:

| File | Purpose |
|---|---|
| `blue-deployment.yml` | Deploys Version A |
| `green-deployment.yml` | Deploys Version B |
| `canary-service.yml` | Creates stable and canary Services |
| `ab-routing.yml` | Configures A/B traffic routing using Istio |

## Step 1: Deploy Version A

Apply the Blue deployment:

```bash id="7x2m9p"
kubectl apply -f kubernetes/blue-deployment.yml
```

Verify the deployment:

```bash id="3k8v5q"
kubectl get pods -n aceest-fitness -l version=blue
```

## Step 2: Deploy Version B

Apply the Green deployment:

```bash id="5n4j2w"
kubectl apply -f kubernetes/green-deployment.yml
```

Verify the deployment:

```bash id="9p6c1r"
kubectl get pods -n aceest-fitness -l version=green
```

Wait until both deployments are ready:

```bash id="2f7h8m"
kubectl rollout status deployment/aceest-fitness-blue -n aceest-fitness
kubectl rollout status deployment/aceest-fitness-green -n aceest-fitness
```

## Step 3: Create Services

Apply the stable and canary Services:

```bash id="4q1w6e"
kubectl apply -f kubernetes/canary-service.yml
```

The stable Service routes requests to Version A, while the canary Service routes requests to Version B.

## Step 4: Configure A/B Routing

Apply the Istio Gateway:

```bash id="8b3m5n"
kubectl apply -f kubernetes/istio-gateway.yml
```

Apply the A/B routing configuration:

```bash id="6d9p2k"
kubectl apply -f kubernetes/ab-routing.yml
```

The routing configuration uses the `x-user-group` HTTP request header:

- **Group A:** Requests containing `x-user-group: A` are routed to Version A.
- **Group B:** Requests containing `x-user-group: B` are routed to Version B.
- **Default:** Requests without either header are routed to Version A.

## Step 5: Test A/B Routing

Send a request for Group A:

```bash id="1m7v4c"
curl -H "x-user-group: A" http://YOUR_INGRESS_IP/
```

Send a request for Group B:

```bash id="5r2k8j"
curl -H "x-user-group: B" http://YOUR_INGRESS_IP/
```

Send a request without a group header:

```bash id="9w3f6h"
curl http://YOUR_INGRESS_IP/
```

Replace `YOUR_INGRESS_IP` with the external IP or address of your Istio ingress gateway.

## Step 6: Verify Routing Configuration

Check the VirtualService:

```bash id="4h8n2q"
kubectl get virtualservice aceest-fitness-ab-testing -n aceest-fitness
```

Check deployments and pods:

```bash id="7j5p1m"
kubectl get deployments -n aceest-fitness
kubectl get pods -n aceest-fitness
```

Check Services:

```bash id="3c9v6k"
kubectl get services -n aceest-fitness
```

## Step 7: Compare Results

Evaluate both application versions using:

- Response time and latency.
- Application errors.
- Resource utilization.
- User experience.
- Functional behavior.

Use the collected results to determine which version should become the primary application version.

## Benefits

- Allows comparison of two application versions.
- Supports user-group-based traffic routing.
- Helps evaluate application changes before full adoption.
- Enables controlled testing without affecting all users.
- Supports data-driven deployment decisions.

## Prerequisites

- Kubernetes cluster.
- Istio installed and configured.
- Istio ingress gateway available.
- Both application deployments running.
- Stable and canary Services configured.
- HTTP requests containing the appropriate user-group header.
