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
st.markdown("---")
st.caption("Upload a driver image to analyze safety risks")

uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image")
    st.markdown("---")

    if st.button("🔍 Analyze Driver Image"):
        with st.spinner("Analyzing driver behavior..."):
            try:
                result = analyze_driver_image(uploaded_file.read())
                
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

                if result['drowsiness'] == "POSSIBLY DROWSY" and result['emotion'] in ["Angry", "Sad"]:
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
                    
            except Exception as e:
                st.error("⚠️ Cannot connect to server. Please make sure the backend is running at http://localhost:8000")
                st.error(f"Error details: {str(e)}")
                st.write("Run this command in another terminal:")
                st.code("python -m uvicorn main:app --reload")

# Footer
st.markdown("---")
st.caption("Driver Safety AI • For safety purposes only")