import numpy as np


def construct_signal(coeficient: list[dict], t: float) -> tuple[np.ndarray, complex]:
    """Evaluates the Fourier series at a given time and returns the phasor chain.


    Args:
        coeficient: List of Fourier coefficient dicts.
            Each dict must contain:

            - ``"frequency"`` (int): Frequency index *n*.
            - ``"c"`` (complex): Complex coefficient value.

        t: Normalized time in the range ``[0, 1)``, where ``0`` and ``1``
            both represent the start of one full period.

    Returns:
        A tuple ``(points, final_pos)`` where:

        - ``points`` (np.ndarray): Complex array of length ``len(coeficient) + 1``
            with the tip position after each phasor is added, starting at the
            origin ``0+0j``.
        - ``final_pos`` (complex): Terminal position of the last phasor,
            equivalent to ``points[-1]``. Represents the reconstructed signal
            value at time ``t``.
    """
    pos = complex(0, 0)
    points = [pos]

    for coef in coeficient:
        n = coef["frequency"]
        c_n = coef["c"]

        pos += c_n * np.exp(2j * np.pi * n * t)
        points.append(pos)

    return np.array(points), pos
