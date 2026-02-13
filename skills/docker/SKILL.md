---
name: docker
description: Docker deployment patterns, debugging zero-output containers, and Oracle Cloud Free Tier VM management. Use when building Dockerfiles, writing docker-compose.yml, deploying to cloud VMs, or debugging containers that don't produce output.
---

# Docker Deployment & Oracle Cloud VMs

## Zero-Output Container Debugging

When a Docker container produces zero logs (`docker logs` shows nothing), **check host resources before reading code.** The most common cause is memory exhaustion — the process never reaches its first log statement.

Diagnostic checklist (run on the host, not inside the container):

```bash
# 1. Check RAM and swap
free -h
# If swap is >90% used, the container is likely thrashing and will never initialize

# 2. Check if OOM killer struck
dmesg | grep -i oom

# 3. Check container exit status
docker inspect <container> --format='{{.State.OOMKilled}} {{.State.ExitCode}}'

# 4. Check disk space (Docker images/volumes fill disk fast)
df -h

# 5. Check what's using memory
docker stats --no-stream
```

**If swap is nearly full and `free` shows <100MB available:** The container is not broken — the host doesn't have enough RAM. Fix the host, not the container.

## Oracle Cloud Free Tier

### Available Instances

| Shape | vCPUs | RAM | Arch | Notes |
|-------|-------|-----|------|-------|
| VM.Standard.E2.1.Micro | 1 | 956 MB | x86_64 | Very tight for Docker workloads |
| VM.Standard.A1.Flex | 1-4 | 6-24 GB | ARM (aarch64) | Much more headroom, Always Free |

**The E2.1.Micro (1GB) is usually too small** for multi-container deployments. A single Node.js gateway can need 450MB+ heap. With Docker daemon (~100MB) and OS (~200MB), you're already at capacity before your container starts.

**Recommendation:** Use the A1.Flex ARM instance with 1 OCPU + 6GB RAM. This is also Always Free and handles multiple containers comfortably. Note: ARM requires `linux/arm64` Docker images — most official Node.js images support this.

### Memory Budgeting

Before deploying, estimate total memory:

| Component | Typical RAM |
|-----------|-------------|
| OS + systemd | 150-200 MB |
| Docker daemon | 80-120 MB |
| Each Node.js container | 100-500 MB (depends on heap) |
| Swap (if configured) | 1-2 GB on disk |

Add it up. If it exceeds physical RAM, you need swap — and if it exceeds RAM + swap, containers will OOM or thrash indefinitely.

### Swap Management

Oracle Cloud VMs often have insufficient or no swap by default. Add swap on memory-constrained instances:

```bash
# Create 2GB swap file
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make persistent across reboots
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Verify
free -h
```

### SSH from Windows Git Bash

Git Bash on Windows mangles Unix-style paths in command arguments. When running SSH commands that include paths like `/home/user`:

```bash
# BAD: Git Bash converts /home/user to C:/Users/...
ssh vm "docker run -e HOME=/home/user ..."

# GOOD: Prefix with MSYS_NO_PATHCONV=1
MSYS_NO_PATHCONV=1 ssh vm "docker run -e HOME=/home/user ..."

# ALSO GOOD: Use double slashes (Git Bash leaves these alone)
ssh vm "docker run -e HOME=//home/user ..."
```

This also affects `schtasks` on Windows — any argument starting with `/` gets mangled.

## Docker Compose Patterns

### Resource Limits

Always set memory limits in `docker-compose.yml` to prevent one container from starving others:

```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 256M
    reservations:
      cpus: '0.1'
      memory: 64M
```

### Config File Management

- **Mutable config** (user edits at runtime): bind-mount from host (`./config:/app/config`)
- **Immutable config** (set at build time): `COPY` into the image in the Dockerfile
- **Secrets** (API keys, tokens): `env_file: .env` in docker-compose.yml, never baked into the image

### Writing Config Files Over SSH

Shell heredocs mangle JSON quotes (especially through SSH layers). Use Python or Node instead:

```bash
# BAD: heredoc may strip quotes depending on shell
cat << 'EOF' > config.json
{"key": "value"}
EOF

# GOOD: Python preserves JSON perfectly
python3 -c "
import json
config = {'key': 'value'}
with open('config.json', 'w') as f:
    json.dump(config, f, indent=2)
"

# ALSO GOOD: Node.js one-liner
node -e "require('fs').writeFileSync('config.json', JSON.stringify({key:'value'}, null, 2))"
```

### Useful Debug Commands

```bash
# View logs (follow mode)
docker compose logs -f <service>

# Shell into running container
docker compose exec <service> sh

# Shell into a fresh container (even if the service won't start)
docker compose run --rm <service> sh

# Check what's running and resource usage
docker compose ps
docker stats --no-stream

# Rebuild without cache (when debugging build issues)
docker compose build --no-cache <service>

# View environment variables inside a container
docker compose exec <service> env
```
