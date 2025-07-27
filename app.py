from flask import Flask, render_template, request
import json

app= Flask(__name__)

def suggest_careers(user_input):
    with open('career_data.json') as f:
       careers = json.load(f)

    scores = []
    for career in careers:
        match_count = sum(1 for kw in career['keywords'] if kw in user_input.lower())
        scores.append((career['career'], match_count))

    scores.sort(key=lambda x: x[1], reverse=True)
    return[career for career, score in scores if score > 0][:3]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result' , methods=['POST'])
def result():
    interests = request.form['interests']
    strengths = request.form['strengths']
    workstyle = request.form['workstyle']

    user_input = f"{interests} {strengths} {workstyle}"
    suggestions = suggest_careers(user_input)

    return render_template('result.html', suggestions=suggestions)

if __name__ =='__main__':
  app.run(debug=True)
