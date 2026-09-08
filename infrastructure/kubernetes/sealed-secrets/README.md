# Sealed Secrets

This directory contains the Sealed Secrets configuration for the ecommerce platform.

## What is Sealed Secrets?

Sealed Secrets is a Kubernetes add-on that encrypts Secrets so they can be safely stored in git. The SealedSecret can be decrypted only by the controller running in the cluster, ensuring that secrets are encrypted at rest in git but available as regular Secrets when deployed.

## Installation

Install the Sealed Secrets controller in your cluster:

```bash
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml
```

## Usage

### 1. Create a regular secret (locally)

```bash
kubectl create secret generic ecommerce-secrets \
  --namespace=ecommerce \
  --dry-run=client \
  --from-literal=DATABASE_USER=postgres \
  --from-literal=DATABASE_PASSWORD=<your-password> \
  --from-literal=JWT_SECRET=<your-jwt-secret> \
  --from-literal=STRIPE_API_KEY=<your-stripe-key> \
  -o yaml > secret.yaml
```

### 2. Seal the secret

```bash
kubeseal --format yaml < secret.yaml > ../base/sealed-secret.yaml
```

### 3. Commit the sealed secret

Commit `../base/sealed-secret.yaml` to git. The plaintext `secret.yaml` must not be committed.

### 4. Deploy to cluster

```bash
kubectl apply -f ../base/sealed-secret.yaml
```

The Sealed Secrets controller will automatically decrypt and create the regular Secret in the cluster.

## Migration from plaintext secrets

The old `infrastructure/kubernetes/base/secret.yaml` contained base64-encoded plaintext secrets. The base Kustomization now references `infrastructure/kubernetes/base/sealed-secret.yaml`. To migrate:

1. Install the Sealed Secrets controller in your cluster
2. Install `kubeseal` CLI: https://github.com/bitnami-labs/sealed-secrets/releases
3. Seal the existing secrets using the process above
4. Generate `infrastructure/kubernetes/base/sealed-secret.yaml` with `kubeseal`
5. Verify the generated file contains `encryptedData`, not plaintext values
6. Remove the temporary plaintext `secret.yaml`

## Rotating secrets

To rotate a secret:

1. Update the sealed secret manifest with new values
2. Re-seal using `kubeseal`
3. Commit and deploy the updated sealed secret
