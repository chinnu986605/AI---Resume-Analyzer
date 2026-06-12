from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

SKILLS = ["python", "java", "c++", "html", "css", "javascript"]

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

def analyze_resume(text):
    found = []
    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    score = len(found) * 15
    missing = [s for s in SKILLS if s not in found]

    return score, found, missing

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        text = extract_text(file)

        score, found, missing = analyze_resume(text)

        return render_template("index.html", score=score, found=found, missing=missing)

    return render_template("index.html", score=None)

if __name__ == "__main__":
    app.run(debug=True)