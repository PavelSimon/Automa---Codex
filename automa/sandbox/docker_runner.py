"""Sandbox adapter (Docker/Podman) — MVP stub.

In production, run user scripts inside a locked-down container, with:
- read-only FS, working dir bind-mount, no NET (if possible)
- CPU/memory limits, seccomp/apparmor profile

This module exposes a simple interface for the scheduler to call.
"""

from typing import Sequence


def run_script(script_path: str, args: Sequence[str] | None = None) -> int:
    """Run a script inside a container (not implemented in MVP).

    Returns exit code (0 on success). For now, this function is a stub.
    """
    # TODO: implement docker/podman invocation with security flags
    print(f"[sandbox] would run: {script_path} {args or []}")
    return 0

