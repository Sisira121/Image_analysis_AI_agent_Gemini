# 🍽 Food Image Analyzer

## Overview
Food Image Analyzer is a Streamlit-based application that leverages AI to analyze food images. It estimates the calorie content, determines whether the food is junk or healthy, and calculates the steps needed to burn those calories. The application utilizes Google Gemini for food analysis and OpenAI GPT for generating concise health advice and motivation.

## Features
- 📸 **Food Image Upload**: Users can upload food images for analysis.
- 🔍 **AI-Powered Analysis**: Google Gemini extracts food name, calorie estimate, junk food classification, and required steps to burn calories.
- 💡 **Health Tips & Motivation**: OpenAI GPT provides brief health insights and motivation.
- 🚀 **Interactive Streamlit UI**: A clean and user-friendly interface for seamless interaction.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **AI Models**:
  - Google Gemini (for food analysis)
  - OpenAI GPT-3.5 Turbo (for health insights)
- **Libraries**:
  - `streamlit`
  - `google.generativeai`
  - `openai`
  - `PIL (Pillow)`
  - `re` (for text parsing)

## Installation & Setup
### Prerequisites
- Python 3.8+
- API keys for Google Gemini and OpenAI GPT

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/food-image-analyzer.git
   cd food-image-analyzer
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure API keys:
   - Set your Google Gemini API key in the `genai.configure(api_key="YOUR_GEMINI_API_KEY")` line.
   - Set your OpenAI API key in the `openai.api_key = "YOUR_OPENAI_API_KEY"` line.

## Usage
1. Run the Streamlit application:
   ```sh
   streamlit run app.py
   ```
2. Upload a food image.
3. Click the "🔍 Analyze Image" button.
4. View estimated calories, junk food classification, and steps needed to burn the calories.
5. Read AI-generated health tips and motivation.

## Project Structure
```
food-image-analyzer/
│── archive/                 # Image dataset (optional)
│── app.py                   # Main application script
│── requirements.txt         # List of dependencies
│── README.md                # Documentation
```

## License
This project is licensed under the MIT License.

## Author
Developed by [Sisira](https://github.com/Sisira121). Contributions and suggestions are welcome!

