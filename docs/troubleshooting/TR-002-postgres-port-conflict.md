# TR-002 - PostgreSQL Port Conflict

## Summary

Enterprise PostgreSQL failed to start because another PostgreSQL container was already bound to TCP port 5432.

---

## Symptoms

```
Bind for :::5432 failed

Port already allocated
```

---

## Root Cause

Another Docker container named

projects-db-1

was already exposing

5432:5432

---

## Resolution

View running containers.

```bash
docker ps
```

Stop the conflicting container.

```bash
docker stop projects-db-1
```

Restart the Enterprise Portal PostgreSQL container.

```bash
docker compose up -d
```

---

## Verification

```bash
docker ps
```

Expected

```
enterprise-dev-postgres
```

---

## Long-Term Recommendation

Assign unique host ports for every development environment.

Example

Enterprise Portal

5432

Training Platform

5433

Monitoring

5434

---

## Revision History

| Date | Version | Author |
|-------|----------|--------|
| 2026-06-30 | 1.0 | Leonard Parker |
