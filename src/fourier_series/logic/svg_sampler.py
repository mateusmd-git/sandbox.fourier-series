from pathlib import Path

import numpy as np
from svgpathtools import svg2paths


def sample_svg(source: str, sample_num: int = 2048) -> np.ndarray:
    """Samples points from SVG paths and returns them as normalized complex coordinates.

    Reads all `<path>` elements from an SVG file, distributes the total number
    of sample points proportionally to each path's arc length, and returns the
    result as a centered and normalized array of complex numbers.

    Args:
        source: Path to the source `.svg` file.
        sample_num: Total number of points to sample across all paths.

    Returns:
        A 1-D complex128 array of shape ``(N,)`` where ``N <= sample_num``,
        with points centered at the origin and scaled so that
        ``np.abs(z).max() == 1``.

    """
    if not isinstance(source, str):
        raise TypeError(f"'source' must be a str, got '{type(source).__name__}'.")

    if not isinstance(sample_num, int):
        raise TypeError(
            f"'sample_num' must be an int, got '{type(sample_num).__name__}'."
        )

    source_file = Path(source)

    if not (source_file.name).endswith(".svg"):
        raise ValueError(
            f"'source' must point to an SVG file, got '{source_file.suffix or 'no extension'}'."
        )

    paths = svg2paths(source)[0]
    if not paths:
        raise RuntimeError(
            f"No <path> elements found in '{source_file.name}'. The file may be empty or use unsupported SVG features."
        )

    total_length = sum(p.length() for p in paths if p.length() > 0)

    points = []
    for path in paths:
        length = path.length()

        if length is None:
            raise RuntimeError(
                "A path returned None for its length. The path may be malformed or unsupported."
            )

        if length == 0:
            continue

        local_n = max(4, int(sample_num * length / total_length))

        for k in range(local_n):
            t = k / local_n
            points.append(path.point(t))

    if len(points) <= 4:
        raise ValueError(
            f"Only {len(points)} point(s) were sampled. At least 5 are required. "
            "Consider increasing 'sample_num' or verifying that the SVG paths have non-zero length."
        )

    z = np.array(points, dtype=complex)
    z -= z.mean()
    z = z.real - 1j * z.imag

    scale = np.abs(z).max()
    z = z / scale if scale > 0 else z

    return z
