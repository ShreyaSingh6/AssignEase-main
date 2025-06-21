import google.generativeai as genai

genai.configure(api_key="AIzaSyBSKyP_sB47LFC_tayP7wz3tEte-03yiZ8")

def get_assignment_help(prompt):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
