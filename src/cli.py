from typing import Annotated

import typer


app = typer.Typer()


@app.command()
def run(
    *,
    host: Annotated[
        str,
        typer.Option(
            help='The host to serve on. For local development in localhost use [blue]127.0.0.1[/blue]. To enable public access, e.g. in a container, use all the IP addresses available with [blue]0.0.0.0[/blue].'  # noqa: E501
        ),
    ] = '0.0.0.0',
    port: Annotated[
        int,
        typer.Option(
            help='The port to serve on. You would normally have a termination proxy on top (another program) handling HTTPS on port [blue]443[/blue] and HTTP on port [blue]80[/blue], transferring the communication to your app.'  # noqa: E501
        ),
    ] = 8000,
    reload: Annotated[
        bool,
        typer.Option(
            help='Enable auto-reload of the server when (code) files change. This is [bold]resource intensive[/bold], use it only during development.'  # noqa: E501
        ),
    ] = False,
    root_path: Annotated[
        str,
        typer.Option(
            help='The root path is used to tell your app that it is being served to the outside world with some [bold]path prefix[/bold] set up in some termination proxy or similar.'  # noqa: E501
        ),
    ] = '',
    proxy_headers: Annotated[
        bool,
        typer.Option(
            help='Enable/Disable X-Forwarded-Proto, X-Forwarded-For, X-Forwarded-Port to populate remote address info.'  # noqa: E501
        ),
    ] = True,
):
    import uvicorn

    from src.logger import CONFIG

    uvicorn.run(
        'src.main:app',
        host=host,
        port=port,
        reload=reload,
        root_path=root_path,
        proxy_headers=proxy_headers,
        log_config=CONFIG,
    )
