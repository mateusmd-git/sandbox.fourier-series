import typer

cli = typer.Typer()


@cli.command()
def main(
    verbose: bool = typer.Option(
        False,
        *["--verbose", "-v"],
        is_flag=True,
        help="Enable verbose mode.",
    ),
    source: str = typer.Option(
        None,
        *["--source", "-i"],
        help="Target SVG file image.",
    ),
    sample: int = typer.Option(
        50,
        *["--sample", "-n"],
        help="Number of samples.",
    ),
) -> int:
    """Main entry point."""
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
