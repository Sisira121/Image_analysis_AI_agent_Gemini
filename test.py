import streamlit as st
import google.generativeai as genai
from PIL import Image
import openai  
import re

# Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Function to analyze image with Gemini
def analyze_food_image(image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content([
        "Analyze this food image and provide: \n"
        "Food Name: (only name)\n"
        "Estimated Calories: (only number)\n"
        "Junk Food Status: (Junk Food or Healthy)\n"
        "Steps Needed to Burn Calories: (1 calorie = 20 steps, only number)",
        image
    ])
    
    return response.text

# Function to extract structured data using regex
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
st.set_page_config(page_title="Food Analyzer", page_icon="🍽", layout="centered")
st.title("🍽 Food Image Analyzer")
st.write("Upload an image to analyze its calories and impact on health.")

# Upload image in Streamlit
uploaded_file = st.file_uploader("📂 Upload a food image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="📸 Uploaded Image", use_column_width=True)

    if st.button("🔍 Analyze Image"):
        with st.spinner("Processing..."):
            result = analyze_food_image(img)

        # Extract structured information
        food_name, calories, junk_status, steps_needed = extract_food_info(result)

        # Get AI motivation and insights
        ai_insights = ai_agent(food_name, junk_status, calories, steps_needed)

        # Display results
        st.subheader("📊 Food Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="🍽 Food Name", value=food_name)
            st.metric(label="🔥 Calories", value=f"{calories} kcal")
        with col2:
            st.metric(label="🍟 Junk Food?", value=junk_status)
            st.metric(label="🚶 Steps Needed", value=f"{steps_needed} steps")

        # Display Motivation & Tips
        st.subheader("💡 Health Tip & Motivation")
        st.info(ai_insights, icon="💪")
