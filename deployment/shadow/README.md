
# Shadow Deployment

## Overview

Shadow Deployment is a deployment strategy in which incoming production traffic is copied and sent to a new application version without affecting the response returned to the user.

The stable version continues to handle normal user requests, while the shadow version processes mirrored traffic in the background.

For ACEest Fitness & Gym, this strategy helps validate a new application version using real request patterns before making it the primary version.

## Configuration

The deployment uses the following Kubernetes resources:

| File | Purpose |
|---|---|
| `blue-deployment.yml` | Runs the stable application version |
| `shadow-deployment.yml` | Runs the shadow application version |
| `canary-service.yml` | Provides the stable Service |
| `shadow-service.yml` | Provides the shadow Service |
| `shadow-routing.yml` | Configures traffic mirroring using Istio |

## Step 1: Deploy Stable Version

Apply the stable deployment:

```bash id="84jyku"
kubectl apply -f kubernetes/blue-deployment.yml
```

Verify the stable pods:

```bash id="4r1b2c"
kubectl get pods -n aceest-fitness -l version=blue
```

## Step 2: Deploy Shadow Version

Apply the shadow deployment:

```bash id="n6w8va"
kubectl apply -f kubernetes/shadow-deployment.yml
```

Verify the shadow pods:

```bash id="2g6q9e"
kubectl get pods -n aceest-fitness -l version=shadow
```

Wait until the shadow deployment is ready:

```bash id="4w3p7f"
kubectl rollout status deployment/aceest-fitness-shadow -n aceest-fitness
```

## Step 3: Create Services

Apply the stable and shadow Services:

```bash id="7c5m2a"
kubectl apply -f kubernetes/canary-service.yml
kubectl apply -f kubernetes/shadow-service.yml
```

The stable Service receives normal traffic, while the shadow Service receives mirrored requests.

## Step 4: Configure Traffic Mirroring

Apply the Istio Gateway:

```bash id="5d9q1k"
kubectl apply -f kubernetes/istio-gateway.yml
```

Apply the shadow routing configuration:

```bash id="3f8v6b"
kubectl apply -f kubernetes/shadow-routing.yml
```

The routing configuration sends:

- 100% of normal traffic to the stable version.
- A mirrored copy of traffic to the shadow version.
- Only the stable version's response back to the user.

## Step 5: Verify Shadow Deployment

Check the VirtualService:

```bash id="6h2k9m"
kubectl get virtualservice aceest-fitness-shadow -n aceest-fitness
```

Check the deployments and pods:

```bash id="8j4p1s"
kubectl get deployments -n aceest-fitness
kubectl get pods -n aceest-fitness
```

Check the Services:

```bash id="9k3m5v"
kubectl get services -n aceest-fitness
```

## Step 6: Evaluate the Shadow Version

Monitor the shadow application for:

- Application errors and exceptions.
- Response times and latency.
- Resource utilization.
- Compatibility with incoming requests.
- Differences in application behavior.

Compare the shadow version's behavior with the stable version before promoting it.

## Benefits

- Tests a new version using production-like traffic.
- Does not affect responses returned to users.
- Helps identify bugs and compatibility issues.
- Reduces the risk of introducing an unstable release.
- Supports validation before production rollout.

## Important Note

Shadow traffic is duplicated, so requests that modify data can cause duplicate operations. ACEest Fitness & Gym uses SQLite and has operations such as adding and deleting clients.

For safe testing, use read-only traffic or configure the shadow application to prevent database writes and other side effects.
