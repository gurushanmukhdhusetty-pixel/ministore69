import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="MiniStore | Premium E-Commerce Hub",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS injection for beautiful UI/UX
st.markdown("""
    <style>
    /* Global background adjustments and typography */
    .stApp {
        background-color: #F9FAFB;
    }
    
    /* Hero Title styling */
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
        margin-bottom: 2.5rem;
    }
    
    /* Product Card grid items */
    .product-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
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
        letter-spacing: 0.05em;
    }
    .product-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    .product-description {
        color: #6B7280; 
        font-size: 0.9rem; 
        min-height: 65px;
        line-height: 1.4;
        margin-bottom: 1rem;
    }
    .product-price-tag {
        font-size: 1.5rem;
        font-weight: 800;
        color: #059669;
        margin-bottom: 0.5rem;
    }
    
    /* Floating support button styling anchored at the bottom-right corner */
    .chat-anchor-container {
        position: fixed;
        bottom: 35px;
        right: 35px;
        z-index: 99999;
    }
    .floating-action-chat {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: #FFFFFF !important;
        padding: 14px 28px;
        border-radius: 50px;
        text-decoration: none !important;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
    }
    .floating-action-chat:hover {
        transform: scale(1.05);
        box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SEED DATA (Realistic Store Catalog)
# ==========================================
# 6 comprehensive, realistic products spanning categories with metadata[cite: 8].
PRODUCTS = [
    {"id": 1, "name": "AeroStride Elite Shoes", "category": "Footwear", "price": 4999, "desc": "Lightweight engineered mesh upper paired with high-responsiveness nitrogen-infused foam."},
    {"id": 2, "name": "Titanium Chronograph", "category": "Accessories", "price": 12499, "desc": "Sleek, scratch-resistant pure titanium housing integrated with Japanese precision movement."},
    {"id": 3, "name": "SonicPulse ANC Headphones", "category": "Electronics", "price": 8999, "desc": "Hybrid active noise cancelling hardware giving a crisp 40-hour deep playback timeline."},
    {"id": 4, "name": "HydroShield Commuter Bag", "category": "Accessories", "price": 3499, "desc": "Waterproof technical ballistic nylon build showcasing a modular 16-inch protective laptop bay."},
    {"id": 5, "name": "LuminaGlow Smart Desk Lamp", "category": "Electronics", "price": 2199, "desc": "App-controlled LED desktop source offering multi-spectrum tuning and wireless phone charging."},
    {"id": 6, "name": "FlexForm Ergonomic Mouse", "category": "Electronics", "price": 1799, "desc": "Hyper-accurate optical tracking matrix tailored inside a fatigue-reducing biological arch design."}
]

# Initialize persistent session state for the cart data tracking
if "cart" not in st.session_state:
    st.session_state.cart = {}

# ==========================================
# 3. SIDEBAR (Categories & Cart Aggregator)
# ==========================================
st.sidebar.title("🎒 MiniStore Panel") [cite: 10]
st.sidebar.markdown("---")

# Dynamic Category Filter 
st.sidebar.subheader("Filter Inventory")
unique_categories = ["All Products"] + list(set(p["category"] for p in PRODUCTS))
selected_category = st.sidebar.selectbox("Choose Category", unique_categories)

st.sidebar.markdown("---")
st.sidebar.subheader("🛒 Live Shopping Cart") [cite: 10]

if not st.session_state.cart:
    st.sidebar.info("Your shopping cart is currently empty.")
else:
    running_total = 0
    for product_id, quantity in list(st.session_state.cart.items()):
        prod_obj = next(p for p in PRODUCTS if p["id"] == product_id)
        subtotal = prod_obj["price"] * quantity
        running_total += subtotal
        
        # Display line item breakdown
        st.sidebar.markdown(f"**{prod_obj['name']}**")
        st.sidebar.markdown(f"*{quantity} × ₹{prod_obj['price']:,}* → **₹{subtotal:,}**")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### **Grand Total: ₹{running_total:,}**")
    
    if st.sidebar.button("Clear Cart Summary", use_container_width=True):
        st.session_state.cart = {}
        st.rerun()

# ==========================================
# 4. MARKETPLACE PRESENTATION GRID
# ==========================================
# Header Sections [cite: 7]
st.markdown('<div class="hero-title">MiniStore Showcase</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Experience next-generation utility goods refined for peak day-to-day performance.</div>', unsafe_allow_html=True)

st.markdown("### ✨ Curated Collection")

# Apply dynamic catalog filtering based on category selection
visible_products = PRODUCTS if selected_category == "All Products" else [p for p in PRODUCTS if p["category"] == selected_category]

# Establish a highly-responsive 3-column layout grid 
product_columns = st.columns(3)
for i, item in enumerate(visible_products):
    column_target = product_columns[i % 3] # Distributes cards cleanly across the columns
    
    with column_target:
        # Markdown HTML Injection block representing stylized item frames [cite: 7]
        st.markdown(f"""
            <div class="product-card">
                <span class="product-tag">{item['category']}</span>
                <div class="product-name">{item['name']}</div>
                <div class="product-description">{item['desc']}</div>
                <div class="product-price-tag">₹{item['price']:,}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Native Streamlit transactional button anchored beneath the raw CSS styling block
        if st.button(f"🛒 Add Item to Cart", key=f"item_btn_{item['id']}", use_container_width=True):
            st.session_state.cart[item['id']] = st.session_state.cart.get(item['id'], 0) + 1
            st.toast(f"Successfully added {item['name']} to your cart!", icon="✅")
            st.rerun()

# ==========================================
# 5. FLOATING COMPONENT ROUTING ANCHOR
# ==========================================
# Inserts a floating action link pointing toward the sub-page within the folder hierarchy[cite: 20, 22].
# Streamlit translates standard multi-page names down into standard low-case URL routes.
st.markdown("""
    <div class="chat-anchor-container">
        <a href="/Support_Chatbot" target="_self" class="floating-action-chat">
            💬 Launch Live Support
        </a>
    </div>
""", unsafe_allow_html=True)
