import os
import base64
import streamlit as st
import pickle
import pandas as pd

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Swiggy Delivery Time Prediction",
    page_icon="🍔",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL AND DATA
# --------------------------------------------------
with open('swiggymodel.pkl', 'rb') as f:
    model = pickle.load(f)

df = pd.read_csv('swiggy_demographic.csv')

# --------------------------------------------------
# BACKGROUND IMAGE + LOGO
# --------------------------------------------------
# Keep these files in the same folder as app.py:
#   background.jpg   -> food photo
#   swiggy_logo.png  -> Swiggy logo (transparent PNG)
def get_base64(path, mime):
    with open(path, 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()


if os.path.exists('background.jpg'):
    bg_url = get_base64('background.jpg', 'image/jpeg')
else:
    bg_url = (
        "https://images.unsplash.com/"
        "photo-1504674900247-0877df9cc836"
        "?auto=format&fit=crop&w=1920&q=80"
    )

if os.path.exists('swiggy_logo.png'):
    logo_url = get_base64('swiggy_logo.png', 'image/png')
else:
    logo_url = ""

# --------------------------------------------------
# DARK THEME CSS
# --------------------------------------------------
st.markdown(f"""
<style>

/* Main background: food image with a lighter dark overlay
   (lower the 0.78 / 0.85 values to show more of the food) */
.stApp {{
    background:
        linear-gradient(
            rgba(8, 9, 11, 0.78),
            rgba(8, 9, 11, 0.85)
        ),
        url("{bg_url}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #F5F5F5;
}}

/* Transparent Swiggy logo watermark (fixed, behind content)
   change opacity to make it fainter or stronger */
.stApp::before {{
    content: "";
    position: fixed;
    top: 50%;
    left: 50%;
    width: 520px;
    height: 520px;
    transform: translate(-50%, -50%);
    background: url("{logo_url}") no-repeat center;
    background-size: contain;
    opacity: 0.07;
    pointer-events: none;
    z-index: 0;
}}

/* Main page spacing */
.block-container {{
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 1rem;
}}

/* Main heading */
h1 {{
    color: #FC8019 !important;
    text-align: center;
    font-size: 40px !important;
    font-weight: 800 !important;
}}

/* Section headings */
h2, h3 {{
    color: #FF9D36 !important;
}}

/* General text */
.stApp p,
.stApp label,
.stApp .stMarkdown,
.stApp [data-testid="stMetricLabel"] {{
    color: #F0F0F0;
}}

/* Food sticker banner */
.food-banner {{
    text-align: center;
    font-size: 32px;
    padding: 4px;
    letter-spacing: 12px;
}}

/* Form panels */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-color: #FC8019 !important;
    border-radius: 14px;
}}

/* Select boxes */
div[data-baseweb="select"] > div {{
    background-color: #191B1F !important;
    border: 1.5px solid #FC8019 !important;
    border-radius: 9px !important;
    color: #FFFFFF !important;
    min-height: 42px;
}}

/* Selected dropdown value */
div[data-baseweb="select"] span {{
    color: #FFFFFF !important;
}}

/* Dropdown arrow */
div[data-baseweb="select"] svg {{
    fill: #FC8019 !important;
    color: #FC8019 !important;
}}

/* Dropdown menu */
div[data-baseweb="popover"],
div[data-baseweb="menu"] {{
    background-color: #191B1F !important;
}}

div[role="listbox"] {{
    background-color: #191B1F !important;
}}

div[role="option"] {{
    background-color: #191B1F !important;
    color: #FFFFFF !important;
}}

div[role="option"]:hover {{
    background-color: #733400 !important;
}}

/* Number input boxes */
div[data-baseweb="input"] > div {{
    background-color: #191B1F !important;
    border: 1.5px solid #FC8019 !important;
    border-radius: 9px !important;
}}

div[data-baseweb="input"] input {{
    color: #FFFFFF !important;
    background-color: transparent !important;
}}

/* Number input controls */
div[data-testid="stNumberInput"] button {{
    background-color: #25272B !important;
    color: #FC8019 !important;
    border: none !important;
}}

/* Prediction button */
.stButton > button {{
    background: linear-gradient(
        90deg,
        #FC8019,
        #FF4B2B
    ) !important;

    color: #FFFFFF !important;
    font-size: 19px !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    min-height: 50px;
    width: 100%;
    transition: 0.25s;
}}

/* Button hover effect */
.stButton > button:hover {{
    background: linear-gradient(
        90deg,
        #FF9D36,
        #FC8019
    ) !important;
    transform: scale(1.01);
    box-shadow: 0 0 15px rgba(252, 128, 25, 0.4);
}}

/* Result metric card */
div[data-testid="stMetric"] {{
    background-color: #141619;
    border: 1.5px solid #FC8019;
    border-radius: 14px;
    padding: 18px;
}}

/* Estimated delivery time */
div[data-testid="stMetricValue"] {{
    color: #FC8019 !important;
    font-weight: 800 !important;
}}

/* Progress bar */
div[data-testid="stProgressBar"] > div {{
    background-color: #30343B;
    border-radius: 10px;
}}

div[data-testid="stProgressBar"] > div > div {{
    background: linear-gradient(
        90deg,
        #FC8019,
        #FF3D00
    ) !important;
}}

/* Dividers */
hr {{
    border-color: #66330F !important;
}}

/* Footer */
.footer {{
    text-align: center;
    color: #BDBDBD;
    font-size: 14px;
    padding: 10px;
}}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    '<div class="food-banner">🍔 🍕 🍟 🥤 🛵</div>',
    unsafe_allow_html=True
)

# Small Swiggy logo above the title
if logo_url:
    st.markdown(
        f'<div style="text-align:center;">'
        f'<img src="{logo_url}" width="90" style="opacity:0.9;"></div>',
        unsafe_allow_html=True
    )

st.title("🧡 Swiggy Delivery Time Predictor")

st.markdown(
    """
    <p style="text-align:center; font-size:18px;">
        Predict your food delivery time in minutes!
    </p>
    <p style="text-align:center; font-size:15px;">
        🍔 Delicious Food &nbsp; • &nbsp;
        ⚡ Faster Delivery &nbsp; • &nbsp;
        📍 Smarter Predictions
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# ORDER AND LOCATION DETAILS
# --------------------------------------------------
st.subheader("📍 Order & Location Details")

col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_city = st.selectbox(
        "🏙️ City",
        sorted(df['city_name'].dropna().unique())
    )

with col2:
    city_type = st.selectbox(
        "🌆 City Type",
        sorted(df['city_type'].dropna().unique())
    )

with col3:
    type_of_order = st.selectbox(
        "🍱 Order Type",
        sorted(df['type_of_order'].dropna().unique())
    )

with col4:
    type_of_vehicle = st.selectbox(
        "🛵 Vehicle Type",
        sorted(df['type_of_vehicle'].dropna().unique())
    )

col5, col6, col7, col8 = st.columns(4)

with col5:
    weather = st.selectbox(
        "🌦️ Weather",
        sorted(df['weather'].dropna().unique())
    )

with col6:
    traffic = st.selectbox(
        "🚦 Traffic",
        sorted(df['traffic'].dropna().unique())
    )

with col7:
    order_day_of_week = st.selectbox(
        "📅 Order Day",
        sorted(df['order_day_of_week'].dropna().unique())
    )

with col8:
    order_time_of_day = st.selectbox(
        "🕒 Time of Day",
        sorted(df['order_time_of_day'].dropna().unique())
    )

festival = st.selectbox(
    "🎉 Festival Day?",
    sorted(df['festival'].dropna().unique())
)

st.divider()

# --------------------------------------------------
# DELIVERY DETAILS
# --------------------------------------------------
st.subheader("📦 Delivery Details")

col9, col10, col11, col12 = st.columns(4)

with col9:
    distance = st.number_input(
        "📍 Distance (km)",
        min_value=0.5,
        max_value=25.0,
        value=5.0,
        step=0.1
    )

with col10:
    pickup_time_minutes = st.number_input(
        "🍳 Pickup Time (min)",
        min_value=1,
        max_value=30,
        value=10
    )

with col11:
    order_time_hour = st.number_input(
        "⏰ Order Hour",
        min_value=0,
        max_value=23,
        value=12
    )

with col12:
    multiple_deliveries = st.number_input(
        "📦 Multiple Deliveries",
        min_value=0,
        max_value=3,
        value=1
    )

st.divider()

# --------------------------------------------------
# RIDER AND DATE DETAILS
# --------------------------------------------------
st.subheader("🛵 Rider & Date Details")

col13, col14, col15, col16 = st.columns(4)

with col13:
    age = st.number_input(
        "👤 Rider Age",
        min_value=18,
        max_value=50,
        value=25
    )

with col14:
    ratings = st.number_input(
        "⭐ Rider Rating",
        min_value=1.0,
        max_value=5.0,
        value=4.5,
        step=0.1
    )

with col15:
    vehicle_condition = st.selectbox(
        "🔧 Vehicle Condition",
        sorted(df['vehicle_condition'].dropna().unique())
    )

with col16:
    order_day = st.number_input(
        "📆 Order Day of Month",
        min_value=1,
        max_value=31,
        value=15
    )

order_month = st.selectbox(
    "🗓️ Order Month",
    sorted(df['order_month'].dropna().unique())
)

st.divider()

# --------------------------------------------------
# PREDICTION BUTTON
# --------------------------------------------------
if st.button("🛵 Predict Delivery Time", use_container_width=True):

    is_weekend = (
        1 if order_day_of_week in ["Saturday", "Sunday"]
        else 0
    )

    # Keep feature names consistent with model training
    input_df = pd.DataFrame({
        'age': [age],
        'ratings': [ratings],
        'distance': [distance],
        'multiple_deliveries': [multiple_deliveries],
        'pickup_time_minutes': [pickup_time_minutes],
        'order_time_hour': [order_time_hour],
        'order_day': [order_day],
        'order_month': [order_month],
        'vehicle_condition': [vehicle_condition],
        'type_of_order': [type_of_order],
        'type_of_vehicle': [type_of_vehicle],
        'weather': [weather],
        'traffic': [traffic],
        'festival': [festival],
        'city_type': [city_type],
        'city_name': [selected_city],
        'order_day_of_week': [order_day_of_week],
        'order_time_of_day': [order_time_of_day],
        'is_weekend': [is_weekend]
    })

    try:
        prediction = model.predict(input_df)[0]

        st.divider()
        st.subheader("🎯 Your Delivery Prediction")

        st.metric(
            label="🕒 Estimated Delivery Time",
            value=f"{prediction:.1f} minutes"
        )

        progress = max(
            0,
            min(int(prediction / 60 * 100), 100)
        )

        st.progress(progress)

        if prediction < 20:
            st.success(
                "⚡ Fast delivery expected! Enjoy your meal!"
            )
            st.balloons()

        elif prediction <= 45:
            st.info(
                "🍔 Your food is on its way. Happy eating!"
            )

        else:
            st.warning(
                "🚦 This delivery may take a while. "
                "Traffic or distance could affect the time."
            )

        st.markdown(
            """
            <div class="food-banner">
                🍔 ❤️ 🍟 &nbsp; Good Food, Good Mood! &nbsp; 🍕 🥤
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Prediction error: {e}")
        st.info(
            "Please check the model's expected feature names "
            "and input data types."
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.markdown(
    """
    <div class="footer">
        ❤️ Made for food lovers &nbsp; | &nbsp;
        🛵 Swiggy Delivery Predictor
        <br><br>
        🍔 Better Food, Better Mood! 🍕
    </div>
    """,
    unsafe_allow_html=True
)