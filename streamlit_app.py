import streamlit as st
import json
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Land Zen AI Health Advisor",
    page_icon="✨",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f0fdf4 0%, #dbeafe 50%, #f3e8ff 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 24px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #059669 0%, #2563eb 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis' not in st.session_state:
    st.session_state.analysis = None

# Symptom options
SYMPTOMS = [
    'Chronic Fatigue', 'Brain Fog', 'Digestive Issues', 'Joint Pain',
    'Anxiety/Depression', 'Skin Problems', 'Sleep Issues', 'Weight Gain',
    'Hormonal Imbalance', 'Low Immunity', 'Headaches', 'Inflammation'
]

def generate_analysis(form_data):
    """Generate health analysis based on form data"""
    energy = int(form_data['energy'])
    sleep = int(form_data['sleep'])
    stress = 10 - int(form_data['stress'])
    symptom_penalty = len(form_data['symptoms']) * 2
    
    base_score = ((energy + sleep + stress) / 3) * 10
    overall_score = max(50, int(base_score - symptom_penalty))
    
    deficiencies = []
    
    if energy < 6 or 'Chronic Fatigue' in form_data['symptoms']:
        deficiencies.append({
            'name': 'Magnesium',
            'severity': 'High',
            'impact': 'Energy production, sleep quality, stress response'
        })
    
    if sleep < 6 or 'Sleep Issues' in form_data['symptoms']:
        deficiencies.append({
            'name': 'Vitamin D3',
            'severity': 'Moderate',
            'impact': 'Immune function, mood regulation, bone health'
        })
    
    if 'Brain Fog' in form_data['symptoms'] or 'Inflammation' in form_data['symptoms']:
        deficiencies.append({
            'name': 'Omega-3 Fatty Acids',
            'severity': 'Moderate',
            'impact': 'Brain function, inflammation reduction, cardiovascular health'
        })
    
    if len(deficiencies) < 3:
        deficiencies.append({
            'name': 'B-Complex Vitamins',
            'severity': 'Low',
            'impact': 'Energy metabolism, nervous system function'
        })
    
    imbalances = []
    
    if int(form_data['stress']) > 6 or energy < 5:
        imbalances.append({
            'system': 'Adrenal System',
            'status': 'Depleted',
            'description': 'Your stress levels suggest adrenal fatigue.'
        })
    
    if 'Digestive Issues' in form_data['symptoms']:
        imbalances.append({
            'system': 'Digestive System',
            'status': 'Compromised',
            'description': 'Digestive issues indicate potential gut dysbiosis.'
        })
    elif len(imbalances) < 2:
        imbalances.append({
            'system': 'Detoxification Pathways',
            'status': 'Sluggish',
            'description': 'Multiple symptoms suggest sluggish detoxification.'
        })
    
    recommendations = [
        'Begin with bio-energetic testing to identify precise deficiencies',
        f'Focus on {deficiencies[0]["name"]}-rich foods',
        'Optimize sleep hygiene: consistent bedtime, dark room',
        'Incorporate stress-reduction practices daily',
        'Consider an elimination diet to identify sensitivities'
    ]
    
    products = [
        {'name': 'Bio-Optimized Magnesium Complex', 'price': 34.99, 'benefit': 'Energy and sleep support'},
        {'name': 'Vitamin D3 + K2 (5000 IU)', 'price': 24.99, 'benefit': 'Immune and mood support'},
        {'name': 'Premium Omega-3 Fish Oil', 'price': 42.99, 'benefit': 'Brain health and inflammation'},
        {'name': 'Adrenal Support Blend', 'price': 39.99, 'benefit': 'Stress resilience'}
    ]
    
    return {
        'overall_score': overall_score,
        'deficiencies': deficiencies[:3],
        'imbalances': imbalances,
        'recommendations': recommendations,
        'products': products[:4]
    }

def main():
    if st.session_state.analysis is None:
        st.markdown("<h1 style='text-align: center;'>✨ Free AI Health Analysis</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 18px;'>Discover what your body needs in 3 minutes</p>", unsafe_allow_html=True)
        
        with st.form("health_assessment"):
            st.subheader("Basic Information")
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name *")
                age = st.number_input("Age *", min_value=18, max_value=100, value=35)
            
            with col2:
                email = st.text_input("Email *")
                gender = st.selectbox("Gender *", ["Select...", "Male", "Female", "Other"])
            
            st.subheader("Wellness Levels")
            
            energy = st.slider("Energy Level", 1, 10, 5)
            sleep = st.slider("Sleep Quality", 1, 10, 5)
            stress = st.slider("Stress Level", 1, 10, 5)
            
            st.subheader("Symptoms")
            symptoms = []
            cols = st.columns(3)
            for idx, symptom in enumerate(SYMPTOMS):
                with cols[idx % 3]:
                    if st.checkbox(symptom, key=f"s_{idx}"):
                        symptoms.append(symptom)
            
            st.subheader("Lifestyle")
            col1, col2 = st.columns(2)
            
            with col1:
                diet = st.selectbox("Diet Type", ["Select...", "Standard", "Mediterranean", "Keto", "Vegan", "Paleo"])
            
            with col2:
                exercise = st.selectbox("Exercise", ["Select...", "Rarely", "1-2x/week", "3-4x/week", "5+x/week"])
            
            goal = st.text_area("Primary Health Goal *", height=100)
            
            submitted = st.form_submit_button("✨ Get My Free Analysis")
            
            if submitted:
                if not name or not email or gender == "Select..." or not goal:
                    st.error("Please fill required fields")
                else:
                    form_data = {
                        'name': name, 'email': email, 'age': age, 'gender': gender,
                        'energy': energy, 'sleep': sleep, 'stress': stress,
                        'symptoms': symptoms, 'diet': diet, 'exercise': exercise, 'goal': goal
                    }
                    
                    with st.spinner("Analyzing..."):
                        analysis = generate_analysis(form_data)
                        st.session_state.analysis = analysis
                        st.rerun()
    
    else:
        analysis = st.session_state.analysis
        
        st.markdown("<h1 style='text-align: center;'>✨ Your Health Analysis</h1>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%); 
                    padding: 40px; border-radius: 16px; color: white; margin: 20px 0;'>
            <h2>Wellness Score</h2>
            <div style='font-size: 64px; font-weight: bold;'>{analysis['overall_score']}<span style='font-size: 32px;'>/100</span></div>
            <p style='margin-top: 16px;'>Bio-energetic testing can identify exact imbalances.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔍 Likely Deficiencies")
        for def_item in analysis['deficiencies']:
            st.markdown(f"""
            <div style='border-left: 4px solid #f97316; padding: 12px; margin: 8px 0; background: white; border-radius: 4px;'>
                <strong>{def_item['name']}</strong> - {def_item['severity']} Priority<br>
                <small>Affects: {def_item['impact']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### ⚡ Bio-Energetic Imbalances")
        for imb in analysis['imbalances']:
            st.info(f"**{imb['system']}** ({imb['status']}): {imb['description']}")
        
        st.markdown("### 📋 Action Steps")
        for idx, rec in enumerate(analysis['recommendations'], 1):
            st.markdown(f"{idx}. {rec}")
        
        st.markdown("### 🛍️ Recommended Products")
        cols = st.columns(2)
        for idx, prod in enumerate(analysis['products']):
            with cols[idx % 2]:
                st.markdown(f"**{prod['name']}** - ${prod['price']}")
                st.caption(prod['benefit'])
        
        st.markdown("---")
        st.markdown("## 📅 Ready for Complete Testing?")
        st.markdown("Bio-energetic testing provides a complete scan of your body's needs.")
        
        if st.button("Book Bio-Energetic Test ($97)", type="primary"):
            st.success("Redirecting to booking...")
            st.markdown("[Click here to book](https://calendly.com)")
        
        if st.button("↻ Take Assessment Again"):
            st.session_state.analysis = None
            st.rerun()

if __name__ == "__main__":
    main()
