import sys


def version_callback(active: bool):
    if not active:
        return

    import importlib.metadata

    version = importlib.metadata.version("gvsbuild")
    print(f"gvsbuild v{version}")
    sys.exit(0)
