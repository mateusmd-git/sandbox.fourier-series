import logging

import typer

from fourier_series.animation import animate
from fourier_series.logic import fourier_coeficient, sample_svg

cli = typer.Typer(add_completion=False)


@cli.command()
def main(
    verbose: bool = typer.Option(
        False,
        *["--verbose", "-v"],
        is_flag=True,
        help="Enable verbose mode.",
    ),
    svg_file: str = typer.Option(
        "",
        *["--source", "-i"],
        help="Target SVG file image.",
    ),
    n_coeficients: int = typer.Option(
        50,
        *["--coeficients", "-n"],
        help="Number of coeficients calculated in the DFT.",
    ),
    samples: int = typer.Option(
        2048,
        *["--samples"],
        help="Number of samples.",
    ),
    num_frames: int = typer.Option(
        600,
        *["--frames"],
        help="Number of frames per cicle.",
    ),
    theme: str = typer.Option(
        "dark",
        *["--color"],
        help="Color theme betwen 'dark' and 'light'.",
    ),
    output_file: str | None = typer.Option(
        None,
        *["--save-as"],
        help="Save the animation as a file.",
    ),
) -> int:
    """Main entry point."""
    logging.basicConfig(level=logging.DEBUG if verbose else logging.WARNING)

    z = sample_svg(svg_file, sample_num=samples)
    coefs = fourier_coeficient(z, n_coefs=n_coeficients)

    animate(coefs, frames=num_frames, theme=theme, save_as=output_file)

    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
