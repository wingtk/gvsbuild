import typer


def version_callback(active: bool):
    if not active:
        return

    import importlib.metadata

    version = importlib.metadata.version("gvsbuild")
    typer.echo(f"gvsbuild v{version}")
    raise typer.Exit()
