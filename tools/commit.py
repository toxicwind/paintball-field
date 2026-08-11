#!/usr/bin/env python3
"""SpectreBand commit/push tool. Usage:
    python3 tools/commit.py "commit message" [--push]
    GH_PUSH_PAT=xxx python3 tools/commit.py "message" --push
"""
import sys, subprocess, os

REPO = "/mnt/agents/output/paintball-field"
PAT = os.environ.get("GH_PUSH_PAT", "")

def run(cmd, cwd=REPO):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

if len(sys.argv) < 2:
    print("Usage: python3 tools/commit.py 'commit message' [--push]")
    sys.exit(1)

msg = sys.argv[1]
push = "--push" in sys.argv

print("=== SPECTREBAND COMMIT TOOL ===")
print(f"Message: {msg[:60]}...")

# Stage
out, err, rc = run("git add -A")
if rc != 0:
    print(f"Stage error: {err}")
    sys.exit(1)

# Commit
out, err, rc = run(f'git commit -m "{msg}"')
print(f"Commit: {out}")
if rc != 0 and "nothing to commit" not in out.lower():
    print(f"Commit error: {err}")
    sys.exit(1)

# Push
if push:
    if not PAT:
        print("ERROR: GH_PUSH_PAT not set")
        sys.exit(1)
    remote = f"https://oauth2:{PAT}@github.com/toxicwind/paintball-field.git"
    out, err, rc = run(f"git push '{remote}' main")
    print(f"Push: {out}")
    if rc != 0:
        print(f"Push error: {err}")
        sys.exit(1)

    # Verify
    local, _, _ = run("git rev-parse HEAD | cut -c1-12")
    remote_head, _, _ = run("git ls-remote --heads origin main | awk '{print $1}' | cut -c1-12")
    print(f"Local:  {local}")
    print(f"Remote: {remote_head}")
    if local == remote_head:
        print("VERIFIED: Synced")
    else:
        print("ERROR: Not synced")
        sys.exit(1)

    # Clean PAT from remote
    run("git remote set-url origin https://github.com/toxicwind/paintball-field.git")
    print("PAT cleaned from remote URL")

print("Done.")
