import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
# All parameters are properly separated by commas to prevent SyntaxErrors.
st.set_page_config(
    page_title="MiniStore | Premium E-Commerce Hub",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS injection for beautiful UI/UX
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
        margin-bottom: 2.5rem;
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
# 2. SEED DATA (6 Realistic Products)
# ==========================================
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
# 3. SIDEBAR (Categories & Live Cart)
# ==========================================
st.sidebar.title("🎒 MiniStore Panel")
st.sidebar.markdown("---")

# Dynamic Category Filter
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
        st.sidebar.success("Cart cleared!")

# ==========================================
# 4. MARKETPLACE PRESENTATION GRID
# ==========================================
st.markdown('<div class="hero-title">MiniStore Showcase</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Experience next-generation utility goods refined for peak day-to-day performance.</div>', unsafe_allow_html=True)

# Robust page link that natively ties into Streamlit's page directory routing
st.page_link("pages/1_Support_Chatbot.py", label="Need help? Chat with MiniStore AI Support Agent", icon="💬")
st.markdown("---")

st.markdown("### ✨ Curated Collection")

# Apply dynamic catalog filtering based on category selection
visible_products = PRODUCTS if selected_category == "All Products" else [p for p in PRODUCTS if p["category"] == selected_category]

# Establish a highly-responsive 3-column layout grid
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
        
        # Native action button handling without forcing explicit layout reruns
        if st.button(f"🛒 Add Item", key=f"item_btn_{item['id']}", use_container_width=True):
            st.session_state.cart[item['id']] = st.session_state.cart.get(item['id'], 0) + 1
            st.toast(f"Added {item['name']} to cart!", icon="✅")
