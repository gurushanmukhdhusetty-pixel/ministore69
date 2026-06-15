import streamlit as st

# ==========================================
# 1. GLOBAL PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="MiniStore | Premium E-Commerce Hub",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium UI/UX CSS styling injection
st.markdown("""
    <style>
    .stApp {
        background-color: #F9FAFB;
    }
    .hero-title {
        font-size: 3rem;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .product-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E5E7EB;
        margin-bottom: 0.5rem;
    }
    .product-tag {
        font-size: 0.75rem;
        color: #2563EB;
        background-color: #EFF6FF;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }
    .product-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.5rem;
    }
    .product-description {
        color: #6B7280; 
        font-size: 0.9rem; 
        min-height: 65px;
        margin-bottom: 1rem;
    }
    .product-price-tag {
        font-size: 1.5rem;
        font-weight: 800;
        color: #059669;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SEED DATA (Store Catalog)
# ==========================================
PRODUCTS = [
    {"id": 1, "name": "AeroStride Elite Shoes", "category": "Footwear", "price": 4999, "desc": "Lightweight engineered mesh upper paired with high-responsiveness nitrogen-infused foam."},
    {"id": 2, "name": "Titanium Chronograph", "category": "Accessories", "price": 12499, "desc": "Sleek, scratch-resistant pure titanium housing integrated with Japanese precision movement."},
    {"id": 3, "name": "SonicPulse ANC Headphones", "category": "Electronics", "price": 8999, "desc": "Hybrid active noise cancelling hardware giving a crisp 40-hour deep playback timeline."},
    {"id": 4, "name": "HydroShield Commuter Bag", "category": "Accessories", "price": 3499, "desc": "Waterproof technical ballistic nylon build showcasing a modular 16-inch protective laptop bay."},
    {"id": 5, "name": "LuminaGlow Smart Desk Lamp", "category": "Electronics", "price": 2199, "desc": "App-controlled LED desktop source offering multi-spectrum tuning and wireless phone charging."},
    {"id": 6, "name": "FlexForm Ergonomic Mouse", "category": "Electronics", "price": 1799, "desc": "Hyper-accurate optical tracking matrix tailored inside a fatigue-reducing biological arch design."}
]

# ==========================================
# 3. INITIALIZE PERSISTENT SESSION STATES
# ==========================================
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I am your rule-based MiniStore Support Desk. Ask me about our catalog items, delivery times, or return policies."}
    ]

# Setup a clean program state tracking tool to handle the floating support button logic natively
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

# Helper routine to programmatically adjust tab index navigation
def switch_to_tab(tab_index):
    st.session_state.active_tab = tab_index
    st.rerun()

# ==========================================
# 4. SIDEBAR ELEMENTS (Filters & Live Cart Summary)
# ==========================================
st.sidebar.title("🎒 MiniStore Panel")
st.sidebar.markdown("---")

# Dynamic Category Selector Filter
st.sidebar.subheader("Filter Inventory")
unique_categories = ["All Products"] + list(set(p["category"] for p in PRODUCTS))
selected_category = st.sidebar.selectbox("Choose Category", unique_categories)

st.sidebar.markdown("---")
st.sidebar.subheader("🛒 Live Shopping Cart")

if not st.session_state.cart:
    st.sidebar.info("Your shopping cart is currently empty.")
else:
    running_total = 0
    for product_id, quantity in list(st.session_state.cart.items()):
        prod_obj = next(p for p in PRODUCTS if p["id"] == product_id)
        subtotal = prod_obj["price"] * quantity
        running_total += subtotal
        
        st.sidebar.markdown(f"**{prod_obj['name']}**")
        st.sidebar.markdown(f"*{quantity} × ₹{prod_obj['price']:,}* → **₹{subtotal:,}**")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### **Grand Total: ₹{running_total:,}**")
    
    if st.sidebar.button("Clear Cart Summary", use_container_width=True):
        st.session_state.cart = {}
        st.rerun()

# ==========================================
# 5. NAVIGATION SPACE VIEWPORTS
# ==========================================
# Build the native view page structures using layout containers
tab_marketplace, tab_support = st.tabs(["🛒 Product Marketplace", "💬 Live Support Center"])

# ------------------------------------------
# TAB VIEW A: PRODUCT SHOWCASE
# ------------------------------------------
with tab_marketplace:
    st.markdown('<div class="hero-title">MiniStore Showcase</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Experience next-generation utility goods refined for peak day-to-day performance.</div>', unsafe_allow_html=True)
    
    st.markdown("### ✨ Curated Collection")
    
    # Filter display output data matrix
    visible_products = PRODUCTS if selected_category == "All Products" else [p for p in PRODUCTS if p["category"] == selected_category]
    
    # Establish responsive 3-column layout grid
    product_columns = st.columns(3)
    for i, item in enumerate(visible_products):
        column_target = product_columns[i % 3]
        
        with column_target:
            st.markdown(f"""
                <div class="product-card">
                    <span class="product-tag">{item['category']}</span>
                    <div class="product-name">{item['name']}</div>
                    <div class="product-description">{item['desc']}</div>
                    <div class="product-price-tag">₹{item['price']:,}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🛒 Add Item", key=f"item_btn_{item['id']}", use_container_width=True):
                st.session_state.cart[item['id']] = st.session_state.cart.get(item['id'], 0) + 1
                st.toast(f"Added {item['name']} to cart!", icon="✅")
                st.rerun()

# ------------------------------------------
# TAB VIEW B: RULE-BASED SUPPORT AGENT
# ------------------------------------------
with tab_support:
    st.title("💬 MiniStore Support Help Desk")
    st.caption("Instant automated answers regarding our current catalog collection, shipping, adjustments, and order systems.")
    st.markdown("---")
    
    # Rule-Based Pattern Classifier Logic Matrix
    def get_rule_based_response(user_query: str) -> str:
        query = user_query.lower().strip()
        
        if any(k in query for k in ["product", "item", "shoe", "watch", "headphone", "backpack", "lamp", "mouse", "catalog", "buy"]):
            return (
                "### MiniStore Official Inventory Catalog:\n\n"
                "1. **AeroStride Elite Shoes** (Footwear) — ₹4,999\n"
                "2. **Titanium Chronograph** (Accessories) — ₹12,499\n"
                "3. **SonicPulse ANC Headphones** (Electronics) — ₹8,999\n"
                "4. **HydroShield Commuter Bag** (Accessories) — ₹3,499\n"
                "5. **LuminaGlow Smart Desk Lamp** (Electronics) — ₹2,199\n"
                "6. **FlexForm Ergonomic Mouse** (Electronics) — ₹1,799\n\n"
                "Which item can I help you find details for?"
            )
        elif any(k in query for k in ["delivery", "ship", "courier", "transit", "post", "days", "arrive"]):
            return "🚚 **Delivery Policy:** All orders ship within 24–48 hours. Metro shipments arrive in 3-5 standard business days. Shipping is completely **free** on all orders over ₹2,000!"
        elif "refund" in query:
            return "💰 **Refund Framework:** Once your returned product passes our standard inspection check, refunds are credited back to your original payment source within 5–7 clearing business days."
        elif any(k in query for k in ["return", "exchange", "replace", "wrong size"]):
            return "🔄 **Returns Policy:** MiniStore operates a stress-free **14-day return and exchange policy**. Ensure tags remain attached and the item is in its original packaging container."
        elif any(k in query for k in ["payment", "pay", "upi", "credit card", "cod", "cash on delivery", "netbanking"]):
            return "💳 **Accepted Payments:** We support Visa, Mastercard, RuPay Cards, UPI gateways (GPay, PhonePe), NetBanking, and Cash on Delivery (COD) with no processing fees."
        elif any(k in query for k in ["status", "track", "where is my order", "order number"]):
            return "📍 **Tracking Status:** When your parcel leaves our logistics hubs, you receive an automated SMS with a tracking link to monitor your order live."
        else:
            return "👋 Welcome! I can assist you with **product details, delivery updates, refunds, returns, payment options, or order tracking**. Could you please specify your request?"

    # Render previous conversation lines sequentially from history state arrays
    for speech in st.session_state.chat_history:
        with st.chat_message(speech["role"]):
            st.markdown(speech["content"])

    # Interactive User Prompt Capture
    if input_prompt := st.chat_input("Type your support question here...", key="chat_input_unique"):
        # Display the user's input
        with st.chat_message("user"):
            st.markdown(input_prompt)
        st.session_state.chat_history.append({"role": "user", "content": input_prompt})
        
        # Calculate matching rule-based reply string
        bot_reply = get_rule_based_response(input_prompt)
        
        # Display the automated agent's reply
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        st.rerun()
