from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "shhuSShh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route("/")
def home_screen():
    """Show survey info/start button."""
    return render_template("survey.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_survey():
    """Clear session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/questions/<int:idx>")
def question_page(idx):
    """Display a question."""
    responses = session.get(RESPONSES_KEY)

    if (len(responses) is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # completed survey
        return redirect("/thanks")

    if (len(responses) != idx):
        # invalid question numbers
        flash(f"Invalid question index: {idx}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[idx]
    return render_template(
        "question.html", question_num=idx, question=question)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    answer = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/thanks")

    else:
        return redirect(f"/questions/{len(responses)}")



@app.route("/thanks")
def complete():
    """Show thank you page."""

    return render_template("thanks.html")