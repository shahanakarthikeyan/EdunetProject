import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import datetime

# --- App Config ---
st.set_page_config(page_title="Smart Solar Panel Dashboard", page_icon="🔆")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Control Panel")
dust_level = st.sidebar.slider("Dust Level (%)", 0, 100, 30)
temperature = st.sidebar.slider("Temperature (°C)", 0, 60, 25)
panel_angle = st.sidebar.slider("Solar Panel Position (°)", 0, 180, 90)

# Reset Button
if st.sidebar.button("🔄 Reset to Optimal (90°)"):
    panel_angle = 90

# Last Cleaning Time
if "last_cleaned" not in st.session_state:
    st.session_state.last_cleaned = "Never"

if dust_level > 70:
    st.session_state.last_cleaned = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- System Actions ---
auto_cleaning = "ON" if dust_level > 70 else "OFF"
cooler_status = "ON" if temperature > 40 else "OFF"

# Calculate Power Efficiency (max at 90°)
power_efficiency = np.cos(np.radians(panel_angle - 90))
power_efficiency = max(power_efficiency, 0)
power_percentage = round(power_efficiency * 100, 1)

# Estimated Output (Assuming 300W peak)
panel_max_output = 300
estimated_output = round(panel_max_output * (power_percentage / 100), 1)

# Backend Storage Level (simulate — depends on sun power)
if "storage_level" not in st.session_state:
    st.session_state.storage_level = 100  # start with full battery

# Simulate storage level
if power_percentage < 30:
    st.session_state.storage_level -= 0.5
    st.session_state.storage_level = max(st.session_state.storage_level, 0)
else:
    st.session_state.storage_level = min(st.session_state.storage_level + 0.5, 100)

# --- System Status Display ---
st.title("🔆 Smart Solar Panel Dashboard")

col1, col2 = st.columns(2)
col1.metric("🚿 Auto Cleaning", auto_cleaning)
col2.metric("❄️ Cooler", cooler_status)

st.write(f"**Last Cleaned:** {st.session_state.last_cleaned}")

# --- Power Generation Progress ---
st.subheader("🔋 Power Generation Efficiency")
st.progress(int(power_percentage))
st.write(f"**Efficiency:** {power_percentage}% at {panel_angle}°")
st.success(f"⚡ Estimated Output: **{estimated_output} W**")

# --- Load and Rotate Solar Panel Image ---
panel_img = Image.open(r"C:\Users\shaha\AppData\Local\Programs\Python\Python312\solarpanel-removebg-preview.png")
panel_img_rotated = panel_img.rotate(panel_angle, expand=True)

fig, ax = plt.subplots(figsize=(6, 6))
ax.axis('off')
ax.set_xlim(0, 600)
ax.set_ylim(0, 600)
ax.imshow(panel_img_rotated, extent=(200, 400, 200, 400))
ax.text(300, 20, 'Ground', ha='center', fontsize=12)
ax.set_title(f"Solar Panel at {panel_angle}°", fontsize=14)
st.pyplot(fig)

# --- Backend Storage Status ---
st.subheader("🔋 Energy Storage Status")

storage_level = round(st.session_state.storage_level, 1)

# Storage bar color indicator
if storage_level > 70:
    storage_color = "green"
elif storage_level > 30:
    storage_color = "orange"
else:
    storage_color = "red"

# Draw custom storage bar
st.markdown(f"""
<div style='border: 2px solid #ddd; padding: 5px; width: 100%;'>
  <div style='background-color: {storage_color}; width: {storage_level}%; padding: 8px 0; text-align: center; color: white;'>
    {storage_level}%
  </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.caption("Thresholds: Dust >70% → Auto Clean | Temp >40°C → Cooler | Optimal Position: 90°")

