# AI-Code-Assistant-for-Data-Science

This is a simple and powerful AI assistant that helps with data science tasks like data cleaning, visualization, and model building using just a CSV file and a text prompt.

You upload your dataset and describe what you want to do, and the app will generate:
- ✅ Suggested cleaning steps
- ✅ Python code (with pandas, seaborn, sklearn)
- ✅ Easy-to-understand explanations for each step

It works with both:
- 🔹 OpenAI models (like GPT-4, GPT-3.5)
- 🔹 Local models using Ollama (like Mistral, Gemma)

---

## 🚀 How to Run the App

```bash
# Clone the repo
git clone https://github.com/your-username/ai-code-assistant.git
cd ai-code-assistant

# Set up virtual environment (optional)
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run the app
streamlit run app.py
