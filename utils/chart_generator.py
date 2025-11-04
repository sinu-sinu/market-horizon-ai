import plotly.graph_objects as go
from typing import Dict
import random


def generate_positioning_map(positioning_data: Dict) -> go.Figure:
    fig = go.Figure()

    companies = positioning_data.get("companies", {})
    for company, coords in companies.items():
        # Base coordinates with small jitter to prevent overlap
        x_val = coords.get("x", 0) + random.uniform(-0.1, 0.1)
        y_val = coords.get("y", 0) + random.uniform(-0.1, 0.1)

        # Add main marker (no text to avoid label overlap)
        fig.add_trace(
            go.Scatter(
                x=[x_val],
                y=[y_val],
                mode="markers",
                name=company,
                marker=dict(size=15, opacity=0.8, line=dict(width=2, color="white")),
                hovertemplate=(
                    f"<b>{company}</b><br>"
                    f"Price: {x_val:.1f}/10<br>"
                    f"Target Size: {y_val:.1f}/10<br>"
                    "<extra></extra>"
                ),
            )
        )

        # Dynamic label position (above if lower half, below if upper half)
        label_y_offset = 0.4 if y_val < 5 else -0.4

        # Add annotation label with background for readability
        fig.add_annotation(
            x=x_val,
            y=y_val + label_y_offset,
            text=company,
            showarrow=False,
            font=dict(size=11, color="black"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=0.5,
            borderpad=2,
        )

    # Opportunity zones (optional visual callouts)
    opportunity_zones = positioning_data.get("opportunity_zones", [])
    for zone in opportunity_zones:
        x = zone["coordinates"].get("x", 0)
        y = zone["coordinates"].get("y", 0)
        fig.add_shape(
            type="circle",
            x0=x - 0.5,
            y0=y - 0.5,
            x1=x + 0.5,
            y1=y + 0.5,
            fillcolor="green",
            opacity=0.2,
            line=dict(color="green", width=2, dash="dash"),
        )
        fig.add_annotation(
            x=x,
            y=y,
            text="💡 Opportunity",
            showarrow=False,
            font=dict(size=10, color="green")
        )

    # Quadrant shading
    fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="lightblue", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=0, x1=11, y1=5, fillcolor="lightcoral", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=11, fillcolor="lightgreen", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=5, x1=11, y1=11, fillcolor="lightyellow", opacity=0.1, line_width=0)

    # Axis labels
    dimensions = positioning_data.get("dimensions", {})
    fig.update_layout(
        title="Competitive Positioning Map",
        xaxis_title=dimensions.get("x_axis", "Price Positioning"),
        yaxis_title=dimensions.get("y_axis", "Target Company Size"),
        xaxis=dict(range=[0, 11], tickvals=list(range(1, 11))),
        yaxis=dict(range=[0, 11], tickvals=list(range(1, 11))),
        showlegend=False,
        hovermode="closest",
        width=900,
        height=600,
    )

    return fig
