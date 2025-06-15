# External Access Configuration

This Helm chart provides multiple ways to expose the Cloud Wranglers website externally:

## 1. Ingress (Recommended)

The primary method for external access is through an NGINX Ingress Controller with automatic SSL certificates.

### Features:
- **Automatic SSL/TLS**: Let's Encrypt certificates via cert-manager
- **Domain routing**: Supports both `cloudwranglers.io` and `www.cloudwranglers.io`
- **Security headers**: HSTS, XSS protection, content type options
- **Rate limiting**: 100 requests per minute per IP
- **Optimized timeouts**: 300 seconds for proxy operations

### Prerequisites:
```bash
# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml
```

### Configuration:
```yaml
ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: "cloudwranglers.io"
    - host: "www.cloudwranglers.io"
  tls:
    enabled: true
```

## 2. LoadBalancer Service (Alternative)

For environments where ingress is not available or as a secondary access method.

### Features:
- **Direct external IP**: Cloud provider assigns external IP
- **No ingress controller required**: Direct L4 load balancing
- **Cloud provider integration**: Works with AWS ELB, GCP GLB, Azure LB

### Configuration:
```yaml
loadBalancer:
  enabled: true
  type: LoadBalancer
  port: 80
  annotations:
    # AWS example:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
```

## 3. Deployment Options

### Option A: Ingress Only (Recommended)
```bash
helm install cloudwranglers ./helm/cloudwranglers \
  --set loadBalancer.enabled=false \
  --set ingress.enabled=true
```

### Option B: LoadBalancer Only
```bash
helm install cloudwranglers ./helm/cloudwranglers \
  --set loadBalancer.enabled=true \
  --set ingress.enabled=false
```

### Option C: Both (Redundancy)
```bash
helm install cloudwranglers ./helm/cloudwranglers \
  --set loadBalancer.enabled=true \
  --set ingress.enabled=true
```

## 4. DNS Configuration

### For Ingress:
1. Get the ingress controller's external IP:
   ```bash
   kubectl get svc -n ingress-nginx ingress-nginx-controller
   ```

2. Create DNS A records:
   ```
   cloudwranglers.io     A    <INGRESS_IP>
   www.cloudwranglers.io A    <INGRESS_IP>
   ```

### For LoadBalancer:
1. Get the LoadBalancer's external IP:
   ```bash
   kubectl get svc cloudwranglers-lb
   ```

2. Create DNS A records:
   ```
   cloudwranglers.io     A    <LOADBALANCER_IP>
   www.cloudwranglers.io A    <LOADBALANCER_IP>
   ```

## 5. Verification

### Check Services:
```bash
kubectl get svc -n cloudwranglers-site
```

### Check Ingress:
```bash
kubectl get ingress -n cloudwranglers-site
```

### Check SSL Certificate:
```bash
kubectl get certificate -n cloudwranglers-site
```

### Test External Access:
```bash
curl -I https://cloudwranglers.io
curl -I https://www.cloudwranglers.io
```

## 6. Security Features

- **Network Policies**: Restrict pod-to-pod communication
- **Security Contexts**: Non-root containers with dropped capabilities
- **HTTPS Enforcement**: Automatic redirect from HTTP to HTTPS
- **HSTS Headers**: Prevent protocol downgrade attacks
- **Rate Limiting**: Protect against abuse

## 7. Troubleshooting

### Common Issues:

1. **Ingress not getting external IP**:
   - Ensure NGINX Ingress Controller is installed
   - Check ingress controller service status

2. **SSL certificate not issuing**:
   - Verify cert-manager is installed and running
   - Check ClusterIssuer status
   - Verify DNS is pointing to ingress IP

3. **LoadBalancer stuck in pending**:
   - Ensure cloud provider supports LoadBalancer services
   - Check cloud provider quotas and permissions

### Debug Commands:
```bash
# Check pod status
kubectl get pods -n cloudwranglers-site

# Check ingress events
kubectl describe ingress -n cloudwranglers-site

# Check certificate status
kubectl describe certificate -n cloudwranglers-site

# Check network policies
kubectl get networkpolicy -n cloudwranglers-site
```