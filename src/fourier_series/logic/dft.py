import numpy as np


def fourier_coeficient(z: np.ndarray, n_coefs: int = 50) -> list[dict]:
    """Computes the Discrete Fourier Transform and returns the dominant coefficients.

    Args:
        z: Complex-valued 1-D array representing the sampled signal.
        n_coefs: Maximum number of coefficients to return after sorting by
            amplitude.

    Returns:
        A list of up to ``n_coefs`` dicts, sorted by ``"amplitude"`` descending.
        Each dict contains:

        - ``"frequency"`` (int): The integer frequency index *n*.
        - ``"amplitude"`` (float): Magnitude of the complex coefficient ``|c_n|``.
        - ``"phase"`` (float): Phase angle of ``c_n`` in radians.
        - ``"c"`` (complex): The raw complex coefficient value.

    """
    N = len(z)

    freqs = list(range(N // 2 + 1)) + list(range(-(N // 2) + 1, 0))
    coeficient = []

    for n in freqs:
        c_n = (1 / N) * sum(z[k] * np.e ** (-2j * np.pi * n * k / N) for k in range(N))

        coeficient.append(
            {
                "frequency": n,
                "amplitude": float(abs(c_n)),
                "phase": float(np.angle(c_n)),
                "c": complex(c_n),
            }
        )

    coeficient.sort(key=lambda x: x["amplitude"], reverse=True)
    return coeficient[:n_coefs]
