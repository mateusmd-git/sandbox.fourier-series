import matplotlib.animation as animation
import numpy as np
from matplotlib import pyplot as plt

from fourier_series.logic import construct_signal


class ColorScheme:
    def __init__(self, bg: str, epicircles: str, arrows: str) -> None:
        self.backgound = bg
        self.epicircles = epicircles
        self.arrows = arrows


THEMES: dict[str, ColorScheme] = {
    "dark": ColorScheme(
        bg="#333132",
        epicircles="#ffffff",
        arrows="#4af0c8",
    ),
    "light": ColorScheme(
        bg="#f5f5f0",
        epicircles="#222222",
        arrows="#d63031",
    ),
}


def animate(
    coeficient: list[dict],
    frames: int = 600,
    theme: str = "dark",
    save_as: str | None = None,
) -> None:
    """Renders an animated Fourier series epicycle visualization.

    Draws a set of rotating phasors whose tip traces a path
    reconstructed from the given Fourier coefficients. Supports dark
    and light themes and optional export to a video file via FFmpeg.

    Args:
        coeficient: List of Fourier coefficient dicts.
        frames: Total number of animation frames.
        theme: Color theme to apply. Accepts ``"dark"`` or ``"light"``.
        save_as: If provided, the animation is saved to this file path using
            FFmpegWriter.
    """
    colors = THEMES.get(theme, THEMES["dark"])

    fig, ax = plt.subplots(figsize=(7, 7), facecolor=colors.backgound)
    ax.set_facecolor(colors.backgound)
    ax.set_aspect("equal")
    ax.axis("off")

    mergin = sum(c["amplitude"] for c in coeficient) * 1.05
    ax.set_xlim(-mergin, mergin)
    ax.set_ylim(-mergin, mergin)

    n_epicircles = len(coeficient)

    arrow_hands = [
        ax.plot([], [], color=colors.arrows, lw=0.8, alpha=0.7)[0]
        for _ in range(n_epicircles)
    ]

    circles = [
        plt.Circle((0, 0), 0, fill=False, color=colors.epicircles, lw=0.3, alpha=0.2)
        for _ in range(n_epicircles)
    ]

    for circ in circles:
        ax.add_patch(circ)

    (arrow_line,) = ax.plot([], [], color="#ff6b6b", lw=1.2, alpha=0.9)

    history_x: list[float] = []
    history_y: list[float] = []
    moments = np.linspace(0, 1, frames, endpoint=False)

    def init():
        """Resets all artists to their empty initial state."""
        for ln in arrow_hands:
            ln.set_data([], [])
        arrow_line.set_data([], [])
        return arrow_hands + [arrow_line] + circles

    def update(frame_idx: int):
        """Updates all artists for a single animation frame."""
        t = moments[frame_idx]
        points_pos, final_pos = construct_signal(coeficient, t)

        for i, coef in enumerate(coeficient):
            x0, y0 = points_pos[i].real, points_pos[i].imag
            x1, y1 = points_pos[i + 1].real, points_pos[i + 1].imag
            arrow_hands[i].set_data([x0, x1], [y0, y1])
            circles[i].center = (x0, y0)
            circles[i].radius = coef["amplitude"]

        history_x.append(final_pos.real)
        history_y.append(final_pos.imag)
        arrow_line.set_data(history_x, history_y)

        return arrow_hands + [arrow_line] + circles

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=frames,
        init_func=init,
        blit=True,
        interval=1000 / 60,  # ~60 fps
    )

    if save_as:
        writer = animation.FFMpegWriter(fps=60, bitrate=1800)
        ani.save(save_as, writer=writer)
    else:
        plt.tight_layout()
        plt.show()

    plt.close(fig)
