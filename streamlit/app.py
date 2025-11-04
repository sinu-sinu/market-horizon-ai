import os
import sys
from datetime import datetime
import time
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


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Market Horizon AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Market Horizon AI")
st.caption("AI-Powered Competitive Intelligence Platform")

# -------------------- INITIALIZE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "selected_query_id" not in st.session_state:
    st.session_state.selected_query_id = None

history = QueryHistory()


# ---- Utility: Add fallback get_latest_result() ----
def get_latest_result_fallback():
    """Safely get the most recent saved result."""
    try:
        recent = history.get_recent_queries(limit=1)
        if recent:
            query_id = recent[0][0]
            result = history.get_query_by_id(query_id)
            return result
    except Exception:
        return None
    return None


# On first load, fetch latest result if available
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    latest_result = get_latest_result_fallback()
    if latest_result:
        st.session_state.current_result = latest_result


# -------------------- DISPLAY RESULTS --------------------
def display_results(result: dict):
    st.success("Analysis Complete")

    # --- Report Metadata ---
    st.subheader("Report Metadata")
    col1, col2, col3 = st.columns(3)
    confidence = result["report_metadata"]["confidence_score"]
    with col1:
        st.metric("Confidence Score", f"{confidence:.2f}")
    with col2:
        st.metric("Total Sources", result["report_metadata"]["total_sources"])
    with col3:
        st.metric("Processing Time (s)", result["report_metadata"]["processing_time_seconds"])

    st.markdown("---")

    # --- Competitors ---
    st.subheader("Identified Competitors")
    competitors = result["validated_insights"].get("competitors", [])
    if competitors:
        st.write(", ".join(competitors))
        st.caption(f"{len(competitors)} competitors identified")
    else:
        st.info("No competitors identified.")

    st.markdown("---")

    # --- Content Themes ---
    st.subheader("Content Themes")
    themes = result["validated_insights"].get("content_themes", [])
    if themes:
        for theme in themes:
            name = theme.get("theme", "Unknown")
            freq = theme.get("frequency", 0)
            sentiment = theme.get("sentiment", 0)
            st.write(f"- **{name}** | Mentions: {freq} | Sentiment: {sentiment:.2f}")
    else:
        st.info("No themes available.")

    st.markdown("---")

    # --- Positioning Map ---
    st.subheader("Competitive Positioning Map")
    positioning_map = result["validated_insights"].get("positioning_map", {})
    if positioning_map:
        fig = generate_positioning_map(positioning_map)
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Positioning map not available.")

    st.markdown("---")

    # --- Recommendations ---
    st.subheader("Content Recommendations")
    recommendations = result["validated_insights"].get("content_recommendations", [])
    if recommendations:
        for rec in recommendations:
            topic = rec.get("topic", "Untitled")
            priority = rec.get("priority", "medium").capitalize()
            st.write(f"- **{topic}** ({priority} priority)")
    else:
        st.info("No recommendations available.")

    st.markdown("---")

    # --- Quality Flags ---
    if result.get("quality_flags"):
        st.subheader("Quality Insights")
        for flag in result["quality_flags"]:
            flag_type = flag.get("type", "info")
            message = flag.get("message", "")
            agent = flag.get("agent", "unknown")

            if flag_type == "warning":
                st.warning(f"{message} (Source: {agent})")
            elif flag_type == "info":
                st.info(f"{message} (Source: {agent})")
            else:
                st.error(f"{message} (Source: {agent})")

        st.markdown("---")

    # --- Export ---
    st.subheader("Export Report")
    markdown_report = generate_markdown_report(result)
    st.download_button(
        label="Download Markdown Report",
        data=markdown_report,
        file_name=f"market_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown",
        width="stretch",
    )
    st.caption(f"Generated at {datetime.now().strftime('%H:%M:%S')}")


# -------------------- LOAD RESULT --------------------
def load_result_from_history(query_id: int):
    """Load a result from history by ID"""
    result = history.get_query_by_id(query_id)
    if result:
        st.session_state.current_result = result
        st.session_state.selected_query_id = query_id
        st.info(f"Loaded previous report: {result.get('query_text', 'Unknown Query')}")
        st.rerun()


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.subheader("Query History")
    st.markdown("---")

    recent = history.get_recent_queries(limit=5)
    if recent:
        for query_id, qtext, timestamp, confidence, competitors in recent:
            short_title = qtext[:35] + "..." if len(qtext) > 35 else qtext
            with st.expander(short_title):
                st.markdown(f"**Time:** {timestamp}")
                if confidence is not None:
                    st.markdown(f"**Confidence:** {confidence:.2f}")
                if competitors:
                    st.markdown(f"**Competitors:** {competitors}")
                if st.button("Load Full Report", key=f"load_{query_id}"):
                    load_result_from_history(query_id)
    else:
        st.info("No queries yet.")

    st.markdown("---")
    st.subheader("Example Queries")
    examples = [
        "CRM tools for real estate agents",
        "Influencer marketing platforms",
        "Project management software for startups",
        "AI-powered analytics tools",
    ]
    for example in examples:
        if st.button(example, key=f"example_{example}", use_container_width=True):
            st.session_state.example_query = example
            st.rerun()


# -------------------- DISPLAY CURRENT RESULT --------------------
if st.session_state.current_result:
    query_text = st.session_state.current_result.get("query_text", "Previous Analysis")
    with st.chat_message("user"):
        st.markdown(query_text)

    with st.chat_message("assistant"):
        display_results(st.session_state.current_result)

    if st.button("Clear Report", key="clear_result"):
        st.session_state.current_result = None
        st.session_state.selected_query_id = None
        st.rerun()


# -------------------- CHAT SECTION --------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input(placeholder="Ask about a market, e.g., 'project management software'")

if "example_query" in st.session_state:
    user_query = st.session_state.example_query
    del st.session_state.example_query

# -------------------- PROCESS QUERY --------------------
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        st.write("Processing your request...")
        orchestrator = AgentOrchestrator()
        start_time = time.time()
        result = orchestrator.run(user_query)
        elapsed = round(time.time() - start_time, 2)
        result["report_metadata"]["processing_time_seconds"] = elapsed
        result["query_text"] = user_query

        st.session_state.current_result = result
        st.session_state.selected_query_id = None

        display_results(result)

    try:
        # Derive short title for sidebar display (e.g. top theme or truncated query)
        short_title = user_query[:50]
        history.save_query(user_query, result, title=short_title)
    except Exception:
        pass

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Analysis complete. Confidence: {result['report_metadata']['confidence_score']:.2f}."
    })
