import os
import sys
from datetime import datetime

import streamlit as st

# Ensure project root is importable when running from streamlit/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from core.orchestrator import AgentOrchestrator
from utils.chart_generator import generate_positioning_map
from utils.report_generator import generate_markdown_report
from utils.query_history import QueryHistory


st.set_page_config(
    page_title="Market Horizon AI",
    page_icon="🔍",
    layout="wide",
)

st.title("Market Horizon AI")
st.subheader("Agentic Market Intelligence System")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

history = QueryHistory()


def display_results(result: dict):
    # Metadata
    with st.expander("Report Metadata", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Confidence Score",
                f"{result['report_metadata']['confidence_score']:.2f}",
            )
        with col2:
            st.metric("Total Sources", result["report_metadata"]["total_sources"])
        with col3:
            st.metric(
                "Processing Time",
                f"{result['report_metadata']['processing_time_seconds']}s",
            )

    # Competitors
    st.header("Identified Competitors")
    competitors = result["validated_insights"].get("competitors", [])
    st.write(", ".join(competitors) if competitors else "No competitors identified.")

    # Content Themes
    st.header("Content Themes")
    themes = result["validated_insights"].get("content_themes", [])
    if themes:
        for theme in themes:
            st.write(f"**{theme.get('theme','')}** - Frequency: {theme.get('frequency','N/A')}")
    else:
        st.info("No themes available.")

    # Positioning Map
    st.header("Competitive Positioning Map")
    positioning_map = result["validated_insights"].get("positioning_map", {})
    if positioning_map:
        fig = generate_positioning_map(positioning_map)
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Positioning map not available.")

    # Recommendations
    st.header("Content Recommendations")
    recommendations = result["validated_insights"].get("content_recommendations", [])
    if recommendations:
        for rec in recommendations:
            topic = rec.get("topic", "Untitled")
            priority = rec.get("priority", "-")
            st.write(f"- **{topic}** (Priority: {priority})")
    else:
        st.info("No recommendations available.")

    # Quality Flags
    if result.get("quality_flags"):
        with st.expander("⚠️ Quality Flags", expanded=False):
            for flag in result["quality_flags"]:
                st.warning(f"{flag['message']} (Agent: {flag['agent']})")

    # Markdown download
    markdown_report = generate_markdown_report(result)
    st.download_button(
        label="Download Markdown Report",
        data=markdown_report,
        file_name=f"market_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown",
    )


with st.sidebar:
    st.header("Query History")
    recent = history.get_recent_queries(limit=5)
    if recent:
        for query_id, qtext, timestamp, confidence, competitors in recent:
            with st.expander(f"{qtext[:40]}..."):
                st.write(f"**Time:** {timestamp}")
                if confidence is not None:
                    st.write(f"**Confidence:** {confidence:.2f}")
                if competitors is not None:
                    st.write(f"**Competitors:** {competitors}")
                # Placeholder for loading previous results if needed later
    else:
        st.caption("No history yet.")

# Render existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input at bottom
user_query = st.chat_input(placeholder="Ask about a market, e.g., CRM tools for real estate agents")

if user_query:
    # Echo user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Assistant processing message
    with st.chat_message("assistant"):
        status_text = st.empty()
        progress_bar = st.progress(0)
        status_text.text("🔍 Research Agent gathering data...")
        progress_bar.progress(20)

        orchestrator = AgentOrchestrator()
        result = orchestrator.run(user_query)

        progress_bar.progress(100)
        status_text.success("✅ Analysis complete!")

        # Render results within the assistant message block
        display_results(result)

    # Persist
    try:
        history.save_query(user_query, result)
    except Exception:
        pass

    # Save a short summary message to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Analysis complete. Confidence: {result['report_metadata']['confidence_score']:.2f}."
    })


