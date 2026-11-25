from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']

        return f"""
        <h2>Hello, {name}!</h2>
        <h3>Your Email: {email}</h3>
        """

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=7000)