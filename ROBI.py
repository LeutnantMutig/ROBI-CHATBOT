from flask import Flask, render_template, url_for, request, redirect  # type: ignore
import mysql.connector  # type: ignore
from datetime import datetime
import google.generativeai as genai  # type: ignore
import html  # <-- added for decoding HTML entities like &#39; and &#34;
import re

# ------------------------------------------------------------------------
genai.configure(api_key="")
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 2048
}
model = genai.GenerativeModel("models/gemini-2.5-flash", generation_config=generation_config)

# ------------------------------------------------------------------------
db = mysql.connector.connect(
    host="localhost",
    user="robi",
    password="Robi@123",
    database="robi"
)
cursor = db.cursor()
# ------------------------------------------------------------------------

app = Flask(__name__)
prompt_list, answer_list = [], []

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        return redirect('/login')
    else:
        return render_template('start.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    global email
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute(f"SELECT password FROM login WHERE id = '{email}'")
        try:
            password_from_db = cursor.fetchall()[0][0]
        except:
            password_from_db = "No id found with that name."

        if password == password_from_db:
            return redirect('/category')
        else:
            return redirect('/')
    else:
        return render_template('login.html')

def add_id(user, password):
    cursor.execute(f"SELECT * FROM login WHERE id = '{user}'")
    temp = cursor.fetchall()
    if len(temp) == 0:
        cursor.execute(f"INSERT INTO login VALUES ('{user}', '{password}')")
        db.commit()

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['email']
        password = request.form['password']
        add_id(name, password)
        return redirect("/category")
    else:
        return render_template('sign_up.html')

@app.route('/category', methods=['POST', 'GET'])
def check():
    global prompt_list, answer_list
    if request.method == 'POST':
        category = request.form['category']
        return redirect(f'/answer/{category}')
    else:
        prompt_list, answer_list = [], []
        return render_template('index.html')

def get_answer(prompt, category):
    """
    Generates a concise answer using Gemini, only if the prompt is relevant to the given category.
    If not, informs the user politely.
    """
    try:
        prompt = prompt.strip()
        category = category.strip()
        # category = re.sub(r"&#39;|&#34|\.", "", category)


        full_prompt = (
            f"You are a helpful assistant specialized in the category '{category}'.\n"
            f"A user has asked:\n\"{prompt}\"\n\n"
            f"Answer only if it's clearly related to the category. "
            f"Otherwise respond with: [UNRELATED]"
        )

        response = model.generate_content(full_prompt)

        reply = response.text.strip()
    

        # Check for unrelated tag
        if "[UNRELATED]" in reply.upper():
            return f"Please ask a question more relevant to the category '{category}'."

        # Decode HTML entities (like &#39; or &#34;)
        reply = html.unescape(reply)

        # Optional: clean markdown (e.g., **bold**)
        reply = reply.replace("**", "")

        return reply

    except Exception as e:
        return f"An error occurred while processing your request: {str(e)}"

@app.route('/answer/<string:category>', methods=['POST', 'GET'])
def chat(category):
    global prompt_list, answer_list
    if request.method == 'POST':
        prompt = request.form['prompt']
        if prompt.lower() == "exit":
            return redirect('/category')
        prompt_list.append(prompt)

        answer_1 = get_answer(prompt, category)
        answer_list.append(answer_1)
        # answer_1 = answer_1.replace('**', ' ')
        # print(answer_list)

        return render_template('chat_v2.html', chat=zip(answer_list, prompt_list))
    else:
        return render_template('chat_v2.html')

if __name__ == "__main__":
    app.run(debug=True)
