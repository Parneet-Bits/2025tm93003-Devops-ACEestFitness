
# Blue-Green Deployment

## Overview

Blue-Green Deployment is a deployment strategy in which two separate application environments are maintained:

- **Blue:** The currently active version of the application.
- **Green:** The new version being prepared for release.

Both versions run simultaneously. Traffic is initially directed to Blue. After validating Green, traffic is switched to Green by updating the Kubernetes Service selector.

For ACEest Fitness & Gym, this strategy enables safer application releases with minimal downtime and quick rollback.

## Configuration

The deployment uses the following Kubernetes resources:

| File | Purpose |
|---|---|
| `blue-deployment.yml` | Deploys the current application version |
| `green-deployment.yml` | Deploys the new application version |
| `blue-green-service.yml` | Controls which version receives traffic |

## Step 1: Deploy Blue Version

Apply the Blue deployment:

```bash
kubectl apply -f kubernetes/blue-deployment.yml
```

Check the Blue pods:

```bash
kubectl get pods -n aceest-fitness -l version=blue
```

## Step 2: Deploy Green Version

Apply the Green deployment:

```bash
kubectl apply -f kubernetes/green-deployment.yml
```

Check the Green pods:

```bash
kubectl get pods -n aceest-fitness -l version=green
```

Wait until both Green replicas are ready:

```bash
kubectl rollout status deployment/aceest-fitness-green -n aceest-fitness
```

## Step 3: Route Traffic to Blue

Initially, the Service selector is configured as:

```yaml
selector:
  app: aceest-fitness
  version: blue
```

Apply the Service:

```bash
kubectl apply -f kubernetes/blue-green-service.yml
```

All incoming traffic is now routed to the Blue deployment.

## Step 4: Switch Traffic to Green

After validating the Green deployment, update the Service selector:

```bash
kubectl patch service aceest-fitness-blue-green \
  -n aceest-fitness \
  -p '{"spec":{"selector":{"app":"aceest-fitness","version":"green"}}}'
```

Verify the Service endpoints:

```bash
kubectl get endpoints aceest-fitness-blue-green -n aceest-fitness
```

Traffic is now routed to Green.

## Step 5: Rollback to Blue

If the Green version encounters issues, switch traffic back to Blue:

```bash
kubectl patch service aceest-fitness-blue-green \
  -n aceest-fitness \
  -p '{"spec":{"selector":{"app":"aceest-fitness","version":"blue"}}}'
```

Verify the Service endpoints:

```bash
kubectl get endpoints aceest-fitness-blue-green -n aceest-fitness
```

## Verification

Check both deployments:

```bash
kubectl get deployments -n aceest-fitness
kubectl get pods -n aceest-fitness
kubectl get services -n aceest-fitness
```

## Benefits

- Enables near-zero-downtime application releases.
- Allows testing the new version before switching traffic.
- Provides quick rollback by changing the Service selector.
- Keeps the old version available during the release.
- Reduces deployment risk by separating release and activation.

## Important Note

Both Blue and Green deployments must be healthy before switching traffic. Ensure that the application versions are compatible with the database schema and shared data.
