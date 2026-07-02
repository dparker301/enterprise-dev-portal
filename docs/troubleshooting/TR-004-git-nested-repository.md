# TR-004 - Nested Git Repository

## Summary

Git reported changes to the "projects" directory but would not commit its contents.

---

## Symptoms

```
modified: projects

no changes added to commit
```

---

## Root Cause

A second Git repository existed inside the parent repository.

```
projects/.git
```

Git interpreted the folder as a nested repository.

---

## Resolution

Locate nested repositories.

```bash
find . -name ".git"
```

Remove the nested repository.

```bash
rm -rf projects/.git
```

Re-add the files.

```bash
git add .
```

Commit.

```bash
git commit
```

---

## Prevention

Always initialize Git only once at the project root.

---

## Revision History

| Date | Version | Author |
|-------|----------|--------|
| 2026-06-30 | 1.0 | Leonard Parker |
