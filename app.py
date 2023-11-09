from flask import Flask, request, render_template, redirect
# from flask_debugtoolbar import DebugToolbarExtension

from surveys import Survey, Question, surveys

app = Flask(__name__)
# app.config['SECRET_KEY'] = "oh-so-secret"

# debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def index():
    return render_template("index.html", surveys=surveys)

@app.route('/<survey_key>/questions/<int:question_index>')
def questions(survey_key, question_index):
    this_survey = surveys[survey_key]
    print(len(responses), question_index)
    if len(responses) >= len(this_survey.questions):
        return render_template("thanks.html")
    if (len(responses) != question_index):
        return redirect(f"/{survey_key}/questions/{len(responses)}")
    this_question = this_survey.questions[question_index]
    return render_template("question.html", question=this_question, question_index=question_index, survey_key=survey_key)

@app.route('/<survey_key>/answer', methods=["POST"])
def answer(survey_key):
    responses.append(request.form["ans"])
    this_survey = surveys[survey_key]
    if len(responses) >= len(this_survey.questions):
        return render_template("thanks.html")
    return redirect(f'/{survey_key}/questions/{len(responses)}')
