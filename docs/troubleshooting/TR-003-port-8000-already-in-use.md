# TR-003 - FastAPI Port 8000 Already In Use

## Summary

The FastAPI application failed to start because TCP port 8000 was already occupied by a previous Uvicorn process.

---

## Symptoms

```
ERROR:

Errno 98

Address already in use
```

---

## Root Cause

A previous Uvicorn process was still running in the background.

---

## Resolution

Identify the process.

```bash
sudo ss -ltnp | grep 8000
```

Terminate it.

```bash
kill PID
```

or

```bash
kill -9 PID
```

Restart the application.

```bash
make run
```

---

## Verification

```bash
curl http://localhost:8000/api/health
```

Expected

```
200 OK
```

---

## Prevention

Always stop Uvicorn before switching projects.

```
CTRL+C
```

Verify no process exists.

```
sudo ss -ltnp | grep 8000
```

---

## Revision History

| Date | Version | Author |
|-------|----------|--------|
| 2026-06-30 | 1.0 | Leonard Parker |
