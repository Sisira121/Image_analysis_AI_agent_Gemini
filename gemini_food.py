import streamlit as st
import google.generativeai as genai
from PIL import Image
import openai  
import re

# Configure Gemini API
genai.configure(api_key="YOUR GEMINI_API_KEY")

# OpenAI API Key
openai.api_key = "YOUR_OPEN_API_KEY"

def analyze_food_image(image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content([
        "Analyze this food image and provide: \n"
        "Food Name: (provide only the name)\n"
        "Estimated Calories: (provide only the number)\n"
        "Junk Food Status: (Junk Food or Healthy)\n"
        "Steps Needed to Burn Calories: (Assume 1 calorie = 20 steps and provide only the number)"
        , image
    ])
    
    return response.text

def extract_food_info(response_text):
    food_name_match = re.search(r"Food Name:\s*(.+)", response_text)
    calories_match = re.search(r"Estimated Calories:\s*(\d+)", response_text)
    junk_status_match = re.search(r"Junk Food Status:\s*(.+)", response_text)
    steps_match = re.search(r"Steps Needed to Burn Calories:\s*(\d+)", response_text)
    
    food_name = food_name_match.group(1).strip() if food_name_match else "Unknown"
    calories_str = calories_match.group(1).strip() if calories_match else "0"
    junk_status = junk_status_match.group(1).strip() if junk_status_match else "Unknown"
    steps_str = steps_match.group(1).strip() if steps_match else "0"

    # Convert to integers safely
    try:
        calories = int(calories_str)
        steps_needed = int(steps_str)
    except ValueError:
        calories, steps_needed = 0, 0

    return food_name, calories, junk_status, steps_needed

# AI Agent for generating concise motivation and tips
def ai_agent(food_name, junk_status, calories, steps_needed):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a nutritionist providing concise health advice."},
            {
                "role": "user",
                "content": f"Food: {food_name}\n"
                           f"Calories: {calories}\n"
                           f"Junk Food: {junk_status}\n"
                           f"Steps to Burn: {steps_needed}\n\n"
                           f"Provide a **brief** (max 2 lines) motivation and a short, actionable health tip."
            }
        ]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.set_page_config(page_title="Food Analyzer", page_icon="🍽", layout="wide")
st.title("🍽 Food Image Analyzer")
st.write("Upload an image to analyze its calories and impact on health.")

# Load Image from File
img = Image.open("archive\\validation\\Fried food\\12.jpg")

# Layout: Image (Left) | Food Analysis (Right)
col1, col2 = st.columns([1, 1])

with col1:
    st.image(img, caption="📸 Uploaded Image", use_container_width=False)
    analyze_button = st.button("🔍 Analyze Image")  # Button below the image

with col2:
    st.subheader("📊 Food Analysis")

    if analyze_button:
        with st.spinner("Processing..."):
            result = analyze_food_image(img)

        # Extract structured information
        food_name, calories, junk_status, steps_needed = extract_food_info(result)

        # Get AI motivation and insights
        ai_insights = ai_agent(food_name, junk_status, calories, steps_needed)

        # Display Food Analysis
        st.markdown(f"""
            <div style="display: flex; flex-direction: column;">
                <div>
                    <h4>🍽 Food Name</h4>
                    <p style="font-size: 18px;"><b>{food_name}</b></p>
                </div>
                <div>
                    <h4>🔥 Calories</h4>
                    <p style="font-size: 18px;"><b>{calories} kcal</b></p>
                </div>
                <div>
                    <h4>🍟 Junk Food?</h4>
                    <p style="font-size: 18px;"><b>{junk_status}</b></p>
                </div>
                <div>
                    <h4>🚶 Steps Needed</h4>
                    <p style="font-size: 18px;"><b>{steps_needed} steps</b></p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Motivation & Tips (Better Structure)
        st.markdown("<h3 style='text-align: center;'>💡 Health Tip & Motivation</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 18px;'><b>{ai_insights}</b></p>", unsafe_allow_html=True)