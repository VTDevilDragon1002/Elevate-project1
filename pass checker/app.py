from flask import Flask, render_template, request, jsonify
import re
import math
import os

app = Flask(__name__)

# ----------------------------
# Load weak password database
# ----------------------------

WEAK_PASSWORD_FILE = "weak_passwords.txt"
weak_passwords = set()

if os.path.exists(WEAK_PASSWORD_FILE):
    with open(WEAK_PASSWORD_FILE, "r", encoding="utf-8", errors="ignore") as f:
        weak_passwords = set(line.strip().lower() for line in f)


# ----------------------------
# Password Entropy Calculation
# ----------------------------

def calculate_entropy(password):

    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"[0-9]", password):
        charset += 10

    if re.search(r"[!@#$%^&*()_\-+=<>?/{}[\]~]", password):
        charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)

    return round(entropy, 2)


# ----------------------------
# Crack Time Estimation
# ----------------------------

def estimate_crack_time(entropy):

    guesses_per_second = 1e9

    combinations = 2 ** entropy

    seconds = combinations / guesses_per_second

    if seconds < 60:
        return f"{seconds:.2f} seconds"

    if seconds < 3600:
        return f"{seconds/60:.2f} minutes"

    if seconds < 86400:
        return f"{seconds/3600:.2f} hours"

    if seconds < 31536000:
        return f"{seconds/86400:.2f} days"

    return f"{seconds/31536000:.2f} years"


# ----------------------------
# Sequential Pattern Detection
# ----------------------------

def detect_sequence(password):

    sequences = [
        "1234567890",
        "abcdefghijklmnopqrstuvwxyz",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]

    password = password.lower()

    for seq in sequences:
        for i in range(len(seq) - 3):
            if seq[i:i+4] in password:
                return True

    return False


# ----------------------------
# Repeated Character Detection
# ----------------------------

def detect_repetition(password):

    if re.search(r"(.)\1{2,}", password):
        return True

    return False


# ----------------------------
# Main Strength Evaluation
# ----------------------------

def evaluate_password(password):

    score = 0
    feedback = []

    length = len(password)

    if length >= 12:
        score += 3
    elif length >= 8:
        score += 2
    else:
        feedback.append("Password should be at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Include numbers")

    if re.search(r"[!@#$%^&*()_\-+=<>?/{}[\]~]", password):
        score += 2
    else:
        feedback.append("Use special characters")

    if password.lower() in weak_passwords:
        feedback.append("This password appears in common password databases")
        score -= 3

    if detect_sequence(password):
        feedback.append("Sequential pattern detected")
        score -= 1

    if detect_repetition(password):
        feedback.append("Repeated characters detected")
        score -= 1

    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)

    if score <= 2:
        strength = "Very Weak"
    elif score <= 4:
        strength = "Weak"
    elif score <= 6:
        strength = "Medium"
    elif score <= 8:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        "strength": strength,
        "score": score,
        "entropy": entropy,
        "crack_time": crack_time,
        "feedback": feedback
    }


# ----------------------------
# Routes
# ----------------------------

@app.route("/")
def index():

    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password required"}), 400

    result = evaluate_password(password)

    return jsonify(result)


# ----------------------------
# Run Server
# ----------------------------

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)