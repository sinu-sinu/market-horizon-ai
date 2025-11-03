import plotly.graph_objects as go
from typing import Dict


def generate_positioning_map(positioning_data: Dict) -> go.Figure:
    fig = go.Figure()

    companies = positioning_data.get("companies", {})
    for company, coords in companies.items():
        x_val = coords.get("x", 0)
        y_val = coords.get("y", 0)
        fig.add_trace(
            go.Scatter(
                x=[x_val],
                y=[y_val],
                mode="markers+text",
                name=company,
                text=company,
                textposition="top center",
                marker=dict(size=15, opacity=0.7, line=dict(width=2, color="white")),
                hovertemplate=(
                    f"<b>{company}</b><br>"
                    f"Price: {x_val:.1f}/10<br>"
                    f"Target Size: {y_val:.1f}/10<br>"
                    "<extra></extra>"
                ),
            )
        )

    # Opportunity zones (optional)
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
            x=x, y=y, text="💡 Opportunity", showarrow=False, font=dict(size=10, color="green")
        )

    # Quadrant shading
    fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="lightblue", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=0, x1=11, y1=5, fillcolor="lightcoral", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=11, fillcolor="lightgreen", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=5, y0=5, x1=11, y1=11, fillcolor="lightyellow", opacity=0.1, line_width=0)

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


