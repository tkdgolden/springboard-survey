from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension

from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

# debug = DebugToolbarExtension(app)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        "Homepage with dropdown options of all the surveys"

        return render_template("index.html", surveys=surveys)
    if request.method == "POST":
        "After a survey has been selected, initialize session variables and begin questionaire"

        session['survey_key'] = request.form['survey']
        session['responses'] = []
        return redirect('/questions/0')

@app.route('/questions/<int:question_index>')
def questions(question_index):
    "Show a form generated from that question's choices, or redirect if the user has gotten to the wrong page"

    this_survey = surveys[session['survey_key']]
    responses = session['responses']
    if len(responses) >= len(this_survey.questions):
        flash("You have completed this survey.")
        return render_template("thanks.html")
    if (len(responses) != question_index):
        flash("Please answer the question")
        return redirect(f"/questions/{len(responses)}")
    this_question = this_survey.questions[question_index]
    return render_template("question.html", question=this_question, question_index=question_index)

@app.route('/answer', methods=["POST"])
def answer():
    "Take user question answer and put it in session data, send them to thanks page if complete, otherwise to next question"
    
    responses = session['responses']
    responses.append(request.form["ans"])
    session["responses"] = responses
    this_survey = surveys[session['survey_key']]
    if len(responses) >= len(this_survey.questions):
        return render_template("thanks.html")
    return redirect(f'/questions/{len(responses)}')
