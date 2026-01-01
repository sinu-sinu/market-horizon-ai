import plotly.graph_objects as go
from typing import Dict
import math


def generate_positioning_map(positioning_data: Dict) -> go.Figure:
    fig = go.Figure()

    companies = positioning_data.get("companies", {})

    # Store used label coordinates for overlap detection
    placed_labels = []

    def find_text_position(x, y, existing, threshold=0.4):
        """
        Simple heuristic: if (x, y) is too close to any existing label, 
        choose another text position to avoid overlap.
        """
        for ex, ey in existing:
            if abs(x - ex) < threshold and abs(y - ey) < threshold:
                # Choose alternate positions to separate labels visually
                dx, dy = x - ex, y - ey
                angle = math.degrees(math.atan2(dy, dx))
                if -45 <= angle <= 45:
                    return "middle right"
                elif 45 < angle <= 135:
                    return "bottom center"
                elif -135 <= angle < -45:
                    return "top center"
                else:
                    return "middle left"
        return "top center"  # default if no overlap found

    for company, coords in companies.items():
        x_val = coords.get("x", 0)
        y_val = coords.get("y", 0)

        # Pick the best non-overlapping text position
        text_position = find_text_position(x_val, y_val, placed_labels)
        placed_labels.append((x_val, y_val))

        fig.add_trace(
            go.Scatter(
                x=[x_val],
                y=[y_val],
                mode="markers+text",
                name=company,
                text=company,
                textposition=text_position,
                textfont=dict(size=12, color="white"),  # works well with dark theme
                marker=dict(
                    size=15,
                    opacity=0.85,
                    color="#1E90FF",  # DodgerBlue
                    line=dict(width=2, color="white"),
                ),
                hovertemplate=(
                    f"<b>{company}</b><br>"
                    f"Price: {x_val:.1f}/10<br>"
                    f"Target Size: {y_val:.1f}/10<br>"
                    "<extra></extra>"
                ),
            )
        )

    # --- Opportunity zones ---
    for zone in positioning_data.get("opportunity_zones", []):
        x = zone["coordinates"].get("x", 0)
        y = zone["coordinates"].get("y", 0)
        fig.add_shape(
            type="circle",
            x0=x - 0.5, y0=y - 0.5, x1=x + 0.5, y1=y + 0.5,
            fillcolor="limegreen", opacity=0.15,
            line=dict(color="lime", width=2, dash="dash"),
        )
        fig.add_annotation(
            x=x, y=y, text="💡 Opportunity", showarrow=False, font=dict(size=10, color="lime")
        )

    # --- Quadrant shading ---
    fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="#1E3A5F", opacity=0.15, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=0, x1=11, y1=5, fillcolor="#5F1E1E", opacity=0.15, line_width=0)
    fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=11, fillcolor="#1E5F3A", opacity=0.15, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=5, x1=11, y1=11, fillcolor="#5F5F1E", opacity=0.15, line_width=0)

    # --- Layout (dark theme) ---
    dims = positioning_data.get("dimensions", {})
    fig.update_layout(
        title=dict(text="Competitive Positioning Map", font=dict(size=20, color="white")),
        xaxis_title=dims.get("x_axis", "Price Positioning"),
        yaxis_title=dims.get("y_axis", "Target Company Size"),
        xaxis=dict(range=[0, 11], tickvals=list(range(1, 11)), color="white", gridcolor="#444"),
        yaxis=dict(range=[0, 11], tickvals=list(range(1, 11)), color="white", gridcolor="#444"),
        showlegend=False,
        hovermode="closest",
        width=900,
        height=600,
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
    )

    return fig
