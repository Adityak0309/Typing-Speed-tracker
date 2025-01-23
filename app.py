from flask import Flask, render_template, request
from time import time

app = Flask(__name__)

# Typing Speed Checker Logic
def calculate_errors(prompt, inwords):
    words = prompt.split()
    errors = 0

    for i in range(len(inwords)):
        if i < len(words):
            if inwords[i] != words[i]:
                errors += 1
        else:
            errors += 1  # Extra words are errors

    return errors


def calculate_speed(inprompt, elapsed_time):
    inwords = inprompt.split()
    twords = len(inwords)
    typing_speed = (twords / elapsed_time) * 60  # Words per minute
    return typing_speed


@app.route("/", methods=["GET", "POST"])
def index():
    prompt = (
        "It is easier to associate a new habit with a new context than to build a new habit "
        "in the face of competing cues. It can be difficult to go to bed early if you watch television "
        "in your bedroom each night. It can be hard to study in the living room without getting distracted "
        "if that's where you always play video games."
    )
    result = None

    if request.method == "POST":
        start_time = float(request.form["start_time"])
        end_time = time()
        user_input = request.form["typed_text"]

        elapsed = round(end_time - start_time, 2)
        speed = round(calculate_speed(user_input, elapsed), 2)
        errors = calculate_errors(prompt, user_input.split())

        result = {
            "time": elapsed,
            "speed": speed,
            "errors": errors,
        }

    # Pass the current timestamp as the start time
    start_time = time()
    return render_template("index.html", prompt=prompt, result=result, start_time=start_time)


if __name__ == "__main__":
    app.run(debug=True)
