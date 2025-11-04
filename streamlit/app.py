import os
import sys
from datetime import datetime
import time
import logging
import streamlit as st

logger = logging.getLogger(__name__)

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

# Scroll to top on every page load
st.markdown(
    """
    <style>
        /* Smooth scroll behavior */
        html, body {
            scroll-behavior: smooth;
        }
        .stApp {
            scroll-behavior: smooth;
        }
        /* Anchor for scroll to top */
        #page-top {
            position: fixed;
            top: 0;
        }
    </style>

    <script>
        // Force scroll to top on page load
        setTimeout(function() {
            window.scrollTo(0, 0);
        }, 0);
    </script>

    <div id="page-top"></div>
    """,
    unsafe_allow_html=True,
)

st.title("Market Horizon AI")
st.caption("AI-Powered Competitive Intelligence Platform")

# -------------------- INITIALIZE --------------------
# Always start with fresh messages on each page load
st.session_state.messages = []

# Don't auto-load previous results - start fresh
if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "selected_query_id" not in st.session_state:
    st.session_state.selected_query_id = None

history = QueryHistory()


# -------------------- DISPLAY RESULTS --------------------
def display_results(result: dict):
    st.success("Analysis Complete")

    try:
        # --- Report Metadata ---
        st.subheader("Report Metadata")
        col1, col2, col3 = st.columns(3)

        report_meta = result.get("report_metadata", {})
        confidence = report_meta.get("confidence_score", 0.0)
        total_sources = report_meta.get("total_sources", 0)
        processing_time = report_meta.get("processing_time_seconds", 0)

        with col1:
            st.metric("Confidence Score", f"{confidence:.2f}")
        with col2:
            st.metric("Total Sources", total_sources)
        with col3:
            st.metric("Processing Time (s)", processing_time)

        st.markdown("---")

        # --- Competitors ---
        st.subheader("Identified Competitors")
        validated = result.get("validated_insights", {})
        competitors = validated.get("competitors", [])
        if competitors:
            st.write(", ".join(str(c) for c in competitors))
            st.caption(f"{len(competitors)} competitors identified")
        else:
            st.info("No competitors identified.")

        st.markdown("---")

        # --- Content Themes ---
        st.subheader("Content Themes")
        themes = validated.get("content_themes", [])
        if themes:
            for theme in themes:
                try:
                    name = theme.get("theme", "Unknown")
                    freq = theme.get("frequency", 0)
                    sentiment = theme.get("sentiment", 0)
                    st.write(f"- **{name}** | Mentions: {freq} | Sentiment: {sentiment:.2f}")
                except (ValueError, TypeError):
                    st.write(f"- {theme}")
        else:
            st.info("No themes available.")

        st.markdown("---")

        # --- Positioning Map ---
        st.subheader("Competitive Positioning Map")
        positioning_map = validated.get("positioning_map", {})
        if positioning_map and len(positioning_map) > 0:
            try:
                fig = generate_positioning_map(positioning_map)
                st.plotly_chart(fig, width="stretch")
            except Exception as e:
                st.warning(f"Could not generate positioning map: {str(e)}")
        else:
            st.info("Positioning map not available.")

        st.markdown("---")

        # --- Recommendations ---
        st.subheader("Content Recommendations")
        recommendations = validated.get("content_recommendations", [])
        if recommendations:
            for rec in recommendations:
                try:
                    topic = rec.get("topic", "Untitled")
                    priority = rec.get("priority", "medium").capitalize()
                    st.write(f"- **{topic}** ({priority} priority)")
                except (ValueError, TypeError):
                    st.write(f"- {rec}")
        else:
            st.info("No recommendations available.")

        st.markdown("---")

        # --- Quality Flags ---
        quality_flags = result.get("quality_flags", [])
        if quality_flags:
            st.subheader("Quality Insights")
            for flag in quality_flags:
                try:
                    flag_type = flag.get("type", "info")
                    message = flag.get("message", "")
                    agent = flag.get("agent", "unknown")

                    if flag_type == "warning":
                        st.warning(f"{message} (Source: {agent})")
                    elif flag_type == "info":
                        st.info(f"{message} (Source: {agent})")
                    elif flag_type == "error":
                        st.error(f"{message} (Source: {agent})")
                except Exception:
                    st.info(str(flag))

            st.markdown("---")

        # --- Export ---
        st.subheader("Export Report")
        try:
            markdown_report = generate_markdown_report(result)
            st.download_button(
                label="Download Markdown Report",
                data=markdown_report,
                file_name=f"market_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                width="stretch",
            )
        except Exception as e:
            st.warning(f"Could not generate markdown report: {str(e)}")

        st.caption(f"Generated at {datetime.now().strftime('%H:%M:%S')}")

    except Exception as e:
        st.error(f"Error displaying results: {str(e)}")
        logger.error(f"Error in display_results: {e}", exc_info=True)


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
        if st.button(example, key=f"example_{example}", width="stretch"):
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
# Utility: Validate query input
def validate_query(query: str) -> tuple[bool, str]:
    """Validate query for edge cases"""
    if not query or not query.strip():
        return False, "Query cannot be empty"
    if len(query) > 5000:
        return False, "Query is too long (max 5000 characters). Please shorten your query."
    return True, ""


if user_query:
    # Validate query
    is_valid, error_msg = validate_query(user_query)
    if not is_valid:
        st.error(f"Invalid query: {error_msg}")
    else:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            orchestrator = AgentOrchestrator()
            start_time = time.time()

            try:
                with st.spinner("Analyzing market..."):
                    result = orchestrator.run(user_query)
                elapsed = round(time.time() - start_time, 2)
                result["report_metadata"]["processing_time_seconds"] = elapsed
                result["query_text"] = user_query

                # Check for empty results
                competitors = result.get("validated_insights", {}).get("competitors", [])
                themes = result.get("validated_insights", {}).get("content_themes", [])
                recommendations = result.get("validated_insights", {}).get("content_recommendations", [])

                has_results = bool(competitors or themes or recommendations)

                if not has_results:
                    st.warning("⚠️ No results found for this query. The market might be niche or undefined. Try a different query.")
                    result["quality_flags"] = result.get("quality_flags", [])
                    result["quality_flags"].append({
                        "type": "warning",
                        "message": "No competitive insights found for this market",
                        "agent": "orchestrator"
                    })

                st.session_state.current_result = result
                st.session_state.selected_query_id = None

                display_results(result)

            except TimeoutError:
                st.error("⏱️ Query processing timed out. This usually means the research agents took too long. Please try again with a simpler query.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                logger.error(f"Error processing query: {e}", exc_info=True)

        try:
            # Only save if we have valid results
            if st.session_state.current_result:
                history.save_query(user_query, st.session_state.current_result)
        except Exception as e:
            logger.warning(f"Failed to save query to history: {e}")

        if st.session_state.current_result:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Analysis complete. Confidence: {st.session_state.current_result['report_metadata']['confidence_score']:.2f}."
            })
