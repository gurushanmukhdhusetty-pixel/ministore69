import streamlit as st
from openai import OpenAI

# Page Config
st.set_page_config(
    page_title="Customer Support | MiniStore",
    page_icon="💬",
    layout="centered"
)

# Safely extract secret OpenAI API token records
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Missing Configuration: Please create `.streamlit/secrets.toml` with your `OPENAI_API_KEY` token entry.")
    st.stop()

# Instantiate the modern OpenAI Client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==========================================
# COMPREHENSIVE AI SYSTEM KNOWLEDGE PROMPT
# ==========================================
SYSTEM_PROMPT = """
You are a highly professional, polite, and efficient AI customer support representative for MiniStore, an premium online e-commerce website.

Here is the exact live product catalog you must use to answer inventory questions:
1. AeroStride Elite Shoes | Category: Footwear | Price: ₹4,999 | Description: Lightweight engineered mesh upper paired with high-responsiveness nitrogen-infused foam.
2. Titanium Chronograph | Category: Accessories | Price: ₹12,499 | Description: Sleek, scratch-resistant pure titanium housing integrated with Japanese precision movement.
3. SonicPulse ANC Headphones | Category: Electronics | Price: ₹8,999 | Description: Hybrid active noise cancelling hardware giving a crisp 40-hour deep playback timeline.
4. HydroShield Commuter Bag | Category: Accessories | Price: ₹3,499 | Description: Waterproof technical ballistic nylon build showcasing a modular 16-inch protective laptop bay.
5. LuminaGlow Smart Desk Lamp | Category: Electronics | Price: ₹2,199 | Description: App-controlled LED desktop source offering multi-spectrum tuning and wireless phone charging.
6. FlexForm Ergonomic Mouse | Category: Electronics | Price: ₹1,799 | Description: Hyper-accurate optical tracking matrix tailored inside a fatigue-reducing biological arch design.

STORE OPERATIONS & POLICIES:
- Delivery/Shipping: Orders are dispatched within 24-48 business hours. Delivery takes 3-5 standard business days across India. Free shipping applies to total invoice charges above ₹2,000.
- Return/Exchange Policy: We operate a stress-free 14-day window policy. Products must be unused, unwashed, with labels attached, inside original packaging boxes.
- Refunds: Once returned goods clear inspection at our fulfillment hubs, the cash amount credits back to the client's original banking payment channel within 5-7 business days.
- Payment Gateways: We support all major Credit/Debit Cards, secure UPI (GPay, Paytm, PhonePe), NetBanking, and Cash on Delivery (COD).
- Order Status: Customers can check shipment tracking status using the real-time link dispatched via automated dispatch SMS confirmations.

STRICT OPERATIONAL GUARDRAILS:
- You are explicitly restricted to handling store catalog questions, shipping tracking, payment gateways, and refund/return policies.
- If a user asks completely unrelated questions (e.g., general world facts, writing python code scripts, drafting random recipes, personal advice), you must politely but firmly refuse to answer and redirect them back to MiniStore help desk operations.
"""

# Title Headers
st.title("🛍️ MiniStore AI Help Desk")
st.caption("Our OpenAI-driven specialist instantly resolves order tracking, catalog descriptions, returns, and policy topics.")

# Back Navigation Link shortcut
st.page_link("app.py", label="↩ Return to Product Marketplace Showcase", icon="🛒")
st.markdown("---")

# Initialize persistent message array histories
if "openai_messages" not in st.session_state:
    st.session_state.openai_messages = [
        {"role": "assistant", "content": "Hello! Welcome to MiniStore Support. How can I assist you with our catalog items, shipping timelines, or refund requests today?"}
    ]

# Render historic message strings 
for message in st.session_state.openai_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture incoming chat prompt string entries
if prompt_input := st.chat_input("Type your store or catalog inquiry here..."):
    
    # Display customer input card
    with st.chat_message("user"):
        st.markdown(prompt_input)
    st.session_state.openai_messages.append({"role": "user", "content": prompt_input})
    
    # Initiate contextual completion processing
    with st.chat_message("assistant"):
        response_box = st.empty()
        
        try:
            # Build current message stream payloads utilizing instructions context parameters
            payload_history = [{"role": "system", "content": SYSTEM_PROMPT}]
            for msg in st.session_state.openai_messages:
                payload_history.append({"role": msg["role"], "content": msg["content"]})
            
            # Execute completion chat creation
            api_completion = client.chat.completions.create(
                model="gpt-4o-mini",  # Highly responsive, cost-effective target model
                messages=payload_history,
                temperature=0.2       # Keep creativity low to ensure factual accuracy
            )
            
            ai_reply = api_completion.choices[0].message.content or "I was unable to construct a response. Please try again."
            response_box.markdown(ai_reply)
            
        except Exception as error_msg:
            ai_reply = f"Apologies, an execution connection error surfaced processing your query: {str(error_msg)}"
            response_box.markdown(ai_reply)
            
    # Commit the AI's response to the conversation history
    st.session_state.openai_messages.append({"role": "assistant", "content": ai_reply})
