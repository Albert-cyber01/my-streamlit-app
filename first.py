import streamlit as st
import math

st.set_page_config(page_title="Lens Thickness Calculator", layout="centered")

st.title("Lens Edge Thickness Calculator")
st.write("Enter your lens parameters below:")

# Input fields
n = st.number_input(
    "Refractive index (n)", min_value=1.50, max_value=2.0, value=1.50, step=0.01, format="%.2f"
)
D_sphere = st.number_input(
    "Sphere power (in D)", min_value=-2000.0, max_value=2000.0, value=500.0, step=25.0
)
D_cylinder = st.number_input(
    "Cylinder power (in D)", min_value=-800.0, max_value=800.0, value=0.0, step=25.0
)
y = st.number_input(
    "Lens width (mm)", min_value=10.0, max_value=100.0, value=50.0, step=1.0
)
bridge_width = st.number_input(
    "Bridge width (mm)", min_value=10.0, max_value=30.0, value=22.0, step=1.0
)
PD = st.number_input(
    "Pupillary distance (sum of both eyes, mm)", min_value=40.0, max_value=80.0, value=64.0, step=0.5
)

if st.button("Calculate"):
    # Auto-convert input to D units if above threshold (assume input in 100D)
    sphere_D = abs(D_sphere) / 100 if abs(D_sphere) > 20 else abs(D_sphere)
    cylinder_D = abs(D_cylinder) / 100 if abs(D_cylinder) > 8 else abs(D_cylinder)
    D = sphere_D + cylinder_D

    if D > 0:
        # Calculate r and s
        r = (n - 1) / D * 1000
        s = r - math.sqrt(max(r**2 - (y/2)**2, 0))

        # Updated frame width calculation
        frame_width = y + bridge_width
        c = (frame_width - PD) / 2

        # Edge thickness
        thickness = s + 1 + 0.15 * c

        # Use average density for simplified estimation
        density = 1.30  # g/cm³

        # Estimate weight (volume * density / 1000 to convert mm³ to g), total for both lenses
        radius = y / 2
        volume_mm3 = math.pi * radius**2 * thickness
        total_weight = 2 * volume_mm3 * density / 1000

        # Estimate real-world object comparison
        if total_weight < 5:
            comparison = "about the weight of a sheet of A4 paper"
        elif total_weight < 10:
            comparison = "similar to a small coin"
        elif total_weight < 15:
            comparison = "like a USB flash drive"
        elif total_weight < 20:
            comparison = "comparable to a pack of chewing gum"
        elif total_weight < 25:
            comparison = "roughly one AA battery"
        elif total_weight < 30:
            comparison = "similar to a golf ball"
        elif total_weight < 35:
            comparison = "like a large egg"
        elif total_weight < 40:
            comparison = "close to a lemon"
        
        # Display results
        st.subheader("Results")
        st.write(f"**Computed edge thickness:** {thickness:.2f} mm (max reference)")
        st.write(f"**Estimated total lens weight (pair):** {total_weight:.2f} g")
        st.write(f"**This is approximately:** {comparison}")
        st.caption("Weight is estimated using an average density of 1.30 g/cm³ for simplified comparison.")
        st.write("*Actual thickness and weight may vary slightly by design and manufacturer.*")
    else:
        st.info("No calculation performed: Sphere and Cylinder powers are both zero.")

# Disclaimer
st.markdown("---")
st.markdown("**Disclaimer:** This tool provides an approximate estimation based on standard formulas. Actual lens thickness and weight may vary depending on manufacturer and design.")
