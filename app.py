from __future__ import annotations

import json

import streamlit as st
from dotenv import load_dotenv

from startup_signal_lab.anthropic_client import analyze_pitch_with_claude

load_dotenv()

st.set_page_config(page_title="Claude Startup Linter", page_icon="🧠", layout="wide")

st.title("Claude Startup Linter")
st.caption("Value prop + product wedge + model routing + eval mindset in one founder-facing demo.")

sample = """Acme Reliability helps AI product teams continuously improve production agents. Today teams bolt a model-powered helper onto the side of their product, manually inspect traces, and miss edge cases in tool descriptions. Acme Reliability embeds recommendations directly in the workflow, exposes precise MCP tools, and keeps sensitive traces behind the customer's data boundary. The goal is always-on optimization like AppDynamics for AI systems, not a one-off prompt tuner."""

pitch = st.text_area("Paste a startup pitch, website copy, or README", value=sample, height=220)
live = st.toggle("Use live Claude API if ANTHROPIC_API_KEY is set", value=False)

if st.button("Analyze startup signal", type="primary"):
    result = analyze_pitch_with_claude(pitch, live=live)
    left, right = st.columns([1, 2])
    with left:
        st.subheader("Signal score")
        st.json(result["score"])
        st.subheader("Model route")
        st.json(result["route"])
        st.metric("Live Claude call", "yes" if result["live"] else "mock/offline")
        if "usage" in result:
            st.caption("Usage")
            st.code(json.dumps(result["usage"], indent=2))
    with right:
        st.subheader("Founder intervention")
        st.markdown(result["response"])
else:
    st.info("Click Analyze startup signal to run the demo.")

st.divider()
st.markdown("""
### Talk track

This is the core job: turn a startup ecosystem touchpoint into an activated builder.
In a live founder room, the win is not that Claude writes nice prose. The win is that
Claude helps the founder make a sharper product and architecture decision inside the event.
""")
