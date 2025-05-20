# Stool Pigeon Deployment Guide

This guide explains how to deploy the Stool Pigeon application on a Kubernetes cluster with persistent storage for the SQLite database.

## Prerequisites

- Docker installed on your development machine
- kubectl installed and configured to access your Kubernetes cluster
- A Kubernetes cluster with a storage class that supports ReadWriteOnce access mode

## Deployment Steps

### 1. Build the Docker Image

```bash
# From the root directory of the project
docker build -t stool-pigeon:latest .
```

For a remote registry, tag and push the image:

```bash
docker tag stool-pigeon:latest your-registry/stool-pigeon:latest
docker push your-registry/stool-pigeon:latest
```

### 2. Update Kubernetes Manifest (if using a remote registry)

If you're using a remote registry, update the `k8s-manifest.yaml` file:

```yaml
# Change this line in the Deployment section
image: your-registry/stool-pigeon:latest
```

### 3. Configure Secret Values

Before deploying, update the secret values in the `k8s-manifest.yaml` file:

```yaml
stringData:
  django-secret-key: "your-random-secret-key"
  google-client-id: "your-google-client-id"
  google-client-secret: "your-google-client-secret"
```

Alternatively, create the secrets separately:

```bash
kubectl create secret generic stool-pigeon-secrets \
  --from-literal=django-secret-key="your-random-secret-key" \
  --from-literal=google-client-id="your-google-client-id" \
  --from-literal=google-client-secret="your-google-client-secret"
```

### 4. Deploy to Kubernetes

```bash
kubectl apply -f k8s-manifest.yaml
```

### 5. Access the Application

The application will be available at the host defined in the Ingress resource:

```
http://stool-pigeon.local
```

You may need to configure DNS or modify your local hosts file to resolve this hostname. Alternatively, you can use port-forwarding for testing:

```bash
kubectl port-forward svc/stool-pigeon-service 8000:80
```

Then access the application at `http://localhost:8000`.

## Persistent Storage

The application uses a Persistent Volume Claim (PVC) to store the SQLite database file. This ensures data persists across pod restarts and rescheduling.

The database is stored at `/data/db/db.sqlite3` within the container.

## Important Notes

1. **Production Security**: Before deploying to production, further security hardening is recommended:
   - Configure proper TLS for the Ingress
   - Limit the `ALLOWED_HOSTS` to specific hostnames
   - Use a more robust database like PostgreSQL

2. **Scaling**: SQLite doesn't support concurrent writes from multiple processes, so this deployment is limited to a single replica. For scaling, consider migrating to PostgreSQL.

3. **Backup**: Implement a regular backup solution for the persistent volume to prevent data loss.

## Troubleshooting

If you encounter issues:

1. Check pod status: `kubectl get pods`
2. View pod logs: `kubectl logs <pod-name>`
3. Check persistent volume claim: `kubectl get pvc`
4. Validate ingress configuration: `kubectl get ingress`