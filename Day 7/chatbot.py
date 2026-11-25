from flask import Flask ,request,render_template

from google import genai

app=Flask(__name__)

client =genai.Client(api_key="")
@app.route("/",methods=["GET","POST"])
def home():
    answer="" 
    if request.method=="POST":
        question=request.form["questions"] ##html store in variable
        response=client.models.generate_content(
            model="gemini-3.6-flash",
            contents=question
        )
        answer=response.text
    return render_template("indexx.html",answer=answer)

if __name__=="__main__":
    app.run(debug=True)