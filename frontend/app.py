import streamlit as st
import requests

st.set_page_config(page_title="Driver Safety AI", layout="centered")

# Simple custom styling
st.markdown("""
<style>
    .big-title {
        font-size: 2.5rem !important; }
    .risk-high { color: #ff0000; font-weight: bold; }
    .risk-moderate { color: #ff9900; font-weight: bold; }
    .risk-low { color: #00aa00; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="big-title">🚗 Driver Risk Assessment System</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("Upload a driver image to analyze safety-related risks")

# File uploader
uploaded_file = st.file_uploader(
    "**Choose an image file** (JPG, PNG, JPEG)",
    type=["jpg", "png", "jpeg"]
)

# Show image preview
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image")
    st.markdown("---")

    if st.button("🔍 **Analyze Driver Image**", type="primary"):
        with st.spinner("Analyzing driver behavior..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    files={"file": uploaded_file}
                )

                if response.status_code != 200:
                    st.error("❌ Analysis failed. Please try again.")
                else:
                    result = response.json()

                    # =============================
                    # RISK SCORE CALCULATION
                    # =============================
                    risk_score = 0

                    if result["drowsiness"] == "DROWSY":
                        risk_score += 40  
                    elif result["drowsiness"] == "POSSIBLY DROWSY":
                        risk_score += 25   

                    if result["smoking_status"] == "Smoking":
                        risk_score += 25

                    if result["seatbelt_status"] == "no_seatbelt":
                        risk_score += 20

                    if result["emotion"] in ["Angry", "Sad"]:
                        risk_score += 15    
                        
                    # -------- Compound Risks (Escalation Layer) --------
                    if result['emotion'] in ["Angry", "Sad"] and result['seatbelt_status'] == "no_seatbelt":
                        risk_score += 10

                    if result['drowsiness'] == "DROWSY" and result['smoking_status'] == "smoking":
                        risk_score += 15

                    if result['drowsiness'] == "POSSIBLY DROWSY" and result['emotion'] in ["Angry" , "Sad"]:
                        risk_score += 10

                    if result['smoking_status'] == "smoking" and result['seatbelt_status'] == "no_seatbelt":
                        risk_score += 10

                    risk_score = min(risk_score, 100)

                    # =============================
                    # DISPLAY RESULTS
                    # =============================
                    st.subheader("📊 Detection Results")
                    
                    # Create two columns for results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 😴 Drowsiness")
                        st.write(f"**{result['drowsiness']}**")
                        
                        st.markdown("---")
                        
                        st.markdown("#### 🚬 Smoking")
                        st.write(f"**{result['smoking_status']}**")
                        st.write(f"Confidence: {result['smoking_confidence']:.1%}")
                    
                    with col2:
                        st.markdown("#### 🧠 Emotion")
                        st.write(f"**{result['emotion']}**")
                        st.write(f"Confidence: {result['emotion_confidence']:.1%}")
                        
                        st.markdown("---")
                        
                        st.markdown("#### 🦺 Seatbelt")
                        seatbelt_display = result['seatbelt_status'].replace('_', ' ').title()
                        st.write(f"**{seatbelt_display}**")
                        st.write(f"Confidence: {result['seatbelt_confidence']:.1%}")
                    
                    st.markdown("---")
                    
                    # =============================
                    # FINAL RISK SCORE
                    # =============================
                    st.subheader("⚠️ Risk Assessment")
                    
                    # Progress bar with score
                    st.progress(risk_score / 100, text=f"Risk Score: {risk_score}/100")
                    
                    # Risk level with colored text
                    if risk_score >= 70:
                        risk_level = "HIGH RISK 🚨"
                        st.markdown(f'<div class="risk-high">{risk_level}</div>', unsafe_allow_html=True)
                        st.error("**Immediate attention required!** Multiple high-risk behaviors detected.")
                        
                    elif risk_score >= 40:
                        risk_level = "MODERATE RISK ⚠️"
                        st.markdown(f'<div class="risk-moderate">{risk_level}</div>', unsafe_allow_html=True)
                        st.warning("**Monitor closely.** Some safety concerns detected.")
                        
                    else:
                        risk_level = "LOW RISK ✅"
                        st.markdown(f'<div class="risk-low">{risk_level}</div>', unsafe_allow_html=True)
                        st.success("**Safe driving detected.** Continue regular monitoring.")
                    
                    # Recommendations section
                    st.markdown("---")
                    st.subheader("💡 Recommendations")
                    
                    recommendations = []
                    
                    if result["drowsiness"] in ["DROWSY", "POSSIBLY DROWSY"]:
                        recommendations.append("• Suggest taking a break")
                    
                    if result["smoking_status"] == "Smoking":
                        recommendations.append("• Remind about no-smoking policy")
                    
                    if result["seatbelt_status"] == "no_seatbelt":
                        recommendations.append("• Fasten seatbelt immediately")
                    
                    if result["emotion"] in ["Angry", "Sad"]:
                        recommendations.append("• Check emotional state before driving")
                    
                    if recommendations:
                        for rec in recommendations:
                            st.info(rec)
                    else:
                        st.success("• No safety recommendations needed")
                        
            except:
                st.error("⚠️ Cannot connect to server. Please make sure the backend is running at http://localhost:8000")
                st.write("Run this command in another terminal:")
                st.code("python -m uvicorn main:app --reload")

# Footer
st.markdown("---")
st.caption("Driver Safety AI • For safety purposes only")