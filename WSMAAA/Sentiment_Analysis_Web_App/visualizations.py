import matplotlib.pyplot as plt
def create_sentiment_chart(counts):
    """
    Create a bar chart showing Positive, Neutral,
    and Negative sentiment counts.
    """

    labels = ["Positive", "Neutral", "Negative"]

    # Read the count for each sentiment
    values = [
        int(counts.get("Positive", 0)),
        int(counts.get("Neutral", 0)),
        int(counts.get("Negative", 0))
    ]

    colors = ["#22C55E", "#64748B", "#EF4444"]

    fig, ax = plt.subplots(figsize=(8, 4.5))

    bars = ax.bar(
        labels,
        values,
        color=colors,
        width=0.55
    )

    ax.set_title(
        "Sentiment Distribution",
        fontsize=16,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel("Sentiment", fontsize=11)
    ax.set_ylabel("Number of Reviews", fontsize=11)

    ax.bar_label(bars, padding=4, fontsize=11)

    ax.set_ylim(0, max(values, default=0) + 1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    return fig
