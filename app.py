import streamlit as st
from agent.core import run_agent

st.set_page_config(
    page_title="Rapier - Market Intelligence Agent",
    page_icon="⚔️",
    layout="wide"
)

# Header
st.title("⚔️ Rapier-Market Intelligence Agent")
st.caption("Payments & Fintech Competitive Intelligence")
st.markdown("---")

# Example Queries Section
st.markdown("### 💡 Example Queries (Click to use)")

example_queries = [
    "Compare Razorpay vs Cashfree vs PayU latest competitive moves",
    "What are the biggest threats to Razorpay from Stripe and Adyen in India?",
    "Give me a market intelligence briefing on UPI and BaaS competition",
    "Latest funding and product updates of Cashfree Payments and PayU India",
    "How is Stripe expanding in the Indian payments market?",
    "Analyze the competitive positioning of Instamojo and CCAvenue"
]

cols = st.columns(2)
for i, query in enumerate(example_queries):
    with cols[i % 2]:
        if st.button(query, use_container_width=True, key=f"example_{i}"):
            st.session_state.query_input = query

st.markdown("---")

# Query Input
query = st.text_input(
    "Enter your market intelligence query:",
    value=st.session_state.get("query_input", ""),
    placeholder="Type your question here or click an example above..."
)

# Run Button
if st.button("Run Rapier", type="primary", use_container_width=True):
    if query.strip():
        with st.spinner("Rapier is gathering real-time intelligence..."):
            try:
                result = run_agent(query)
                st.markdown("### 📊 Final Intelligence Report")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a query or select an example.")

# Footer
st.markdown("---")
st.caption("Built for Razorpay AI Buildathon 2026 | Rapier tracks: Razorpay, Cashfree, PayU, Stripe, Adyen, PayPal, Instamojo, CCAvenue")