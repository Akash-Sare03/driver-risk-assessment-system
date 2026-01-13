import streamlit as st
from core.analyze import analyze_driver_image

st.set_page_config(page_title="Driver Safety AI", layout="centered")

st.markdown("""
<style>
.big-title { font-size: 2.5rem; }
.risk-high { color: red; font-weight: bold; }
.risk-moderate { color: orange; font-weight: bold; }
.risk-low { color: green; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="big-title">🚗 Driver Risk Assessment System</h1>', unsafe_allow_html=True)
st.caption("Upload a driver image to analyze safety risks")

uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image")

    if st.button("🔍 Analyze Driver Image"):
        with st.spinner("Analyzing driver behavior..."):
            result = analyze_driver_image(uploaded_file.read())

        # ---------------- Risk Score ----------------
        risk_score = 0

        if result["drowsiness"] == "DROWSY":
            risk_score += 40
        elif result["drowsiness"] == "POSSIBLY DROWSY":
            risk_score += 25

        if result["smoking_status"] == "smoking":
            risk_score += 25

        if result["seatbelt_status"] == "no_seatbelt":
            risk_score += 20

        if result["emotion"] in ["Angry", "Sad"]:
            risk_score += 15

        risk_score = min(risk_score, 100)

        # ---------------- Display ----------------
        st.subheader("📊 Detection Results")

        col1, col2 = st.columns(2)

        with col1:
            st.write("😴 **Drowsiness**")
            st.write(result["drowsiness"])

            st.write("🚬 **Smoking**")
            st.write(result["smoking_status"])
            st.write(f"Confidence: {result['smoking_confidence']:.1%}")

        with col2:
            st.write("🧠 **Emotion**")
            st.write(result["emotion"])
            st.write(f"Confidence: {result['emotion_confidence']:.1%}")

            st.write("🦺 **Seatbelt**")
            st.write(result["seatbelt_status"])
            st.write(f"Confidence: {result['seatbelt_confidence']:.1%}")

        st.subheader("⚠️ Risk Assessment")
        st.progress(risk_score / 100)
        st.write(f"Risk Score: {risk_score}/100")

        if risk_score >= 70:
            st.markdown('<div class="risk-high">HIGH RISK 🚨</div>', unsafe_allow_html=True)
        elif risk_score >= 40:
            st.markdown('<div class="risk-moderate">MODERATE RISK ⚠️</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="risk-low">LOW RISK ✅</div>', unsafe_allow_html=True)
