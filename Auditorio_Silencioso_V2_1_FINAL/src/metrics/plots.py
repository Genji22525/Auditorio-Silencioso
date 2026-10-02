from pathlib import Path
import matplotlib.pyplot as plt

def _bar(labels, values, title, ylabel, path):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, values)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)

def generate_comparison_plots(summary, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    engines = list(summary)

    _bar(
        engines,
        [summary[e]["detection_rate"]["mean"] * 100 for e in engines],
        "Taxa de detecção — CTI × SBD",
        "Taxa (%)",
        output_dir / "detection_rate.png",
    )

    _bar(
        engines,
        [summary[e]["coverage"]["mean"] * 100 for e in engines],
        "Cobertura média — CTI × SBD",
        "Cobertura (%)",
        output_dir / "coverage.png",
    )

    ttd = [
        summary[e]["ttd"]["mean"]
        if summary[e]["ttd"]["mean"] is not None
        else 0
        for e in engines
    ]

    _bar(
        engines,
        ttd,
        "Tempo médio até detecção (TTD)",
        "Segundos",
        output_dir / "ttd.png",
    )

    ttc = [
        summary[e]["ttc"]["mean"]
        if summary[e]["ttc"]["mean"] is not None
        else 0
        for e in engines
    ]

    _bar(
        engines,
        ttc,
        "Tempo médio até contenção (TTC)",
        "Segundos",
        output_dir / "ttc.png",
    )