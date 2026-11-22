
# Kubernetes Deployment Strategies

## 1. Introduction

ACEest Fitness & Gym uses Kubernetes to manage application deployments. Multiple deployment strategies are included to demonstrate different approaches to releasing application updates while maintaining availability and reducing deployment risks.

The project implements:

1. Rolling Update
2. Blue-Green Deployment
3. Canary Deployment
4. Shadow Deployment
5. A/B Testing

## 2. Rolling Update Deployment

### Description

Rolling Update gradually replaces existing application pods with new pods. Kubernetes creates new pods and terminates old pods while maintaining application availability.

### Configuration

- Replicas: 2
- Max Surge: 1
- Max Unavailable: 0

### Implementation

Configuration file: `kubernetes/deployment.yml`

Apply the deployment:

```bash
kubectl apply -f kubernetes/deployment.yml
```

Monitor the rollout:

```bash
kubectl rollout status deployment/aceest-fitness -n aceest-fitness
```

### Rollback

```bash
kubectl rollout undo deployment/aceest-fitness -n aceest-fitness
```

### Advantages

- Minimizes downtime.
- Gradually replaces application pods.
- Supports deployment rollback.
- Uses Kubernetes native deployment functionality.

## 3. Blue-Green Deployment

### Description

Blue-Green deployment maintains two independent application versions.

- Blue represents the currently active version.
- Green represents the new version.

Traffic is initially directed to Blue. After validating Green, traffic is switched using the Kubernetes Service selector.

### Configuration Files

- `kubernetes/blue-deployment.yml`
- `kubernetes/green-deployment.yml`
- `kubernetes/blue-green-service.yml`

### Implementation

Deploy Blue:

```bash
kubectl apply -f kubernetes/blue-deployment.yml
```

Deploy Green:

```bash
kubectl apply -f kubernetes/green-deployment.yml
```

Switch traffic to Green:

```bash
kubectl patch service aceest-fitness-blue-green \
  -n aceest-fitness \
  -p '{"spec":{"selector":{"app":"aceest-fitness","version":"green"}}}'
```

### Rollback

Switch the Service selector back to Blue:

```bash
kubectl patch service aceest-fitness-blue-green \
  -n aceest-fitness \
  -p '{"spec":{"selector":{"app":"aceest-fitness","version":"blue"}}}'
```

### Advantages

- Allows validation before release.
- Provides quick rollback.
- Keeps both application versions available.
- Reduces deployment risk.

## 4. Canary Deployment

### Description

Canary deployment releases a new application version to a small percentage of incoming traffic while the majority continues using the stable version.

This project uses Istio to distribute traffic between stable and canary application versions.

### Configuration Files

- `kubernetes/blue-deployment.yml`
- `kubernetes/green-deployment.yml`
- `kubernetes/canary-service.yml`
- `kubernetes/canary-routing.yml`
- `kubernetes/istio-gateway.yml`

### Traffic Distribution

The initial configuration distributes traffic as follows:

- Stable version: 90%
- Canary version: 10%

### Implementation

Apply the stable and canary deployments:

```bash
kubectl apply -f kubernetes/blue-deployment.yml
kubectl apply -f kubernetes/green-deployment.yml
```

Apply Services and routing:

```bash
kubectl apply -f kubernetes/canary-service.yml
kubectl apply -f kubernetes/istio-gateway.yml
kubectl apply -f kubernetes/canary-routing.yml
```

### Promotion and Rollback

After evaluating the canary version, traffic weights can be updated to promote it to 100%.

If problems occur, traffic can be redirected to the stable version by setting its weight to 100%.

### Advantages

- Limits exposure to new application versions.
- Helps identify issues before full deployment.
- Supports gradual releases.
- Enables controlled traffic distribution.

## 5. Shadow Deployment

### Description

Shadow deployment duplicates incoming production requests and forwards them to a new application version without using its responses for actual user requests.

The stable application continues serving users, while the shadow version processes mirrored traffic for validation.

### Configuration Files

- `kubernetes/blue-deployment.yml`
- `kubernetes/shadow-deployment.yml`
- `kubernetes/canary-service.yml`
- `kubernetes/shadow-service.yml`
- `kubernetes/shadow-routing.yml`
- `kubernetes/istio-gateway.yml`

### Implementation

Deploy the stable and shadow versions:

```bash
kubectl apply -f kubernetes/blue-deployment.yml
kubectl apply -f kubernetes/shadow-deployment.yml
```

Apply Services and routing:

```bash
kubectl apply -f kubernetes/canary-service.yml
kubectl apply -f kubernetes/shadow-service.yml
kubectl apply -f kubernetes/istio-gateway.yml
kubectl apply -f kubernetes/shadow-routing.yml
```

### Traffic Behavior

- 100% of normal traffic goes to the stable version.
- A mirrored copy of traffic is sent to the shadow version.
- The shadow response is not returned to the user.

### Advantages

- Tests new versions using production-like requests.
- Does not directly affect user-facing responses.
- Helps identify functional and performance issues.
- Allows validation before promotion.

### Important Consideration

Mirrored requests can execute database writes and other side effects. The shadow application must use read-only operations or an isolated data environment to prevent duplicate modifications.

## 6. A/B Testing Deployment

### Description

A/B testing routes different user groups to different application versions. This allows the team to compare application behavior and performance.

This implementation uses Istio header-based routing.

### Configuration Files

- `kubernetes/blue-deployment.yml`
- `kubernetes/green-deployment.yml`
- `kubernetes/canary-service.yml`
- `kubernetes/ab-routing.yml`
- `kubernetes/istio-gateway.yml`

### Traffic Routing

| User Group | Request Header | Destination |
|---|---|---|
| Group A | `x-user-group: A` | Stable version |
| Group B | `x-user-group: B` | Canary version |
| Default | No matching header | Stable version |

### Implementation

Apply the deployments:

```bash
kubectl apply -f kubernetes/blue-deployment.yml
kubectl apply -f kubernetes/green-deployment.yml
```

Apply Services and routing:

```bash
kubectl apply -f kubernetes/canary-service.yml
kubectl apply -f kubernetes/istio-gateway.yml
kubectl apply -f kubernetes/ab-routing.yml
```

### Testing

Test Group A:

```bash
curl -H "x-user-group: A" http://YOUR_INGRESS_IP/
```

Test Group B:

```bash
curl -H "x-user-group: B" http://YOUR_INGRESS_IP/
```

### Advantages

- Enables comparison of application versions.
- Supports user-group-based routing.
- Helps evaluate new functionality.
- Supports data-driven release decisions.

## 7. Comparison of Deployment Strategies

| Strategy | Traffic Handling | Main Purpose |
|---|---|---|
| Rolling Update | Gradual pod replacement | Continuous application updates |
| Blue-Green | Switches between two versions | Safe version replacement |
| Canary | Percentage-based traffic split | Gradual release |
| Shadow | Duplicates requests | Validate new version without using its responses |
| A/B Testing | Header-based user routing | Compare application versions |

## 8. Conclusion

The deployment strategies demonstrate different approaches to application releases using Kubernetes and Istio. Each strategy provides a different level of control over traffic, testing, and rollback.

These strategies help improve deployment reliability and provide flexibility when releasing new versions of ACEest Fitness & Gym.
