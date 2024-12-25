from flask import Flask, render_template, request, redirect, url_for
import random
import requests

app = Flask(__name__)

# Function to fetch puzzles from an API
import html

# Function to fetch puzzles from an API
def fetch_puzzle():
    try:
        # Example API endpoint (replace with a real riddle/logic puzzle API if available)
        response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
        data = response.json()
        if data["response_code"] == 0:
            question_data = data["results"][0]
            question = html.unescape(question_data["question"])  # Decode HTML entities
            correct_answer = html.unescape(question_data["correct_answer"])  # Decode HTML entities
            options = [html.unescape(opt) for opt in question_data["incorrect_answers"]] + [correct_answer]
            random.shuffle(options)
            return {
                "question": question,
                "answer": correct_answer,
                "options": options
            }
    except Exception as e:
        print("Error fetching puzzle:", e)
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    feedback = ""
    if request.method == "POST":
        user_answer = request.form.get("answer")
        correct_answer = request.form.get("correct_answer")
        if user_answer == correct_answer:
            feedback = "Correct! Well done 🎉"
        else:
            feedback = "Incorrect! Better luck next time."

    # Fetch a random puzzle from the API
    puzzle = fetch_puzzle()
    if not puzzle:
        puzzle = {
            "question": "Error fetching puzzle. Try again later.",
            "answer": "",
            "options": []
        }
    return render_template("index.html", puzzle=puzzle, feedback=feedback)

@app.route("/skip")
def skip():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
