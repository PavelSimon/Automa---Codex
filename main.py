import os
import sys
import uvicorn


def main() -> None:
    # Safer defaults on Windows when using reload (uses multiprocessing)
    reload_flag = os.getenv("AUTOMA_RELOAD", "1") == "1"
    if os.name == "nt":
        # Ensure multiprocessing works reliably on Windows
        import multiprocessing as mp
        mp.freeze_support()
        # Some stacks prefer Selector policy on Windows
        try:
            import asyncio
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore[attr-defined]
        except Exception:
            pass
        # Default reload off unless explicitly enabled
        reload_flag = os.getenv("AUTOMA_RELOAD", "0") == "1"

    if reload_flag:
        app_ref = "automa.api.app:app"
    else:
        # Avoid import-from-string path issues when not reloading
        from automa.api.app import app as app_ref  # type: ignore

    uvicorn.run(
        app_ref,
        host="0.0.0.0",
        port=7999,
        reload=reload_flag,
        log_level=os.getenv("UVICORN_LOG_LEVEL", "info"),
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Surface full error for easier debugging on Windows subprocess
        import traceback
        traceback.print_exc()
        sys.exit(1)
