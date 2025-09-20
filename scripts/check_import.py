import traceback


def main() -> None:
    try:
        import importlib
        m = importlib.import_module("automa.api.app")
        app = getattr(m, "app", None)
        print("IMPORT_OK", bool(app))
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()

