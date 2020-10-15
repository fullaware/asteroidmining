from flask import Flask, render_template, jsonify, request
app = Flask(__name__, static_folder='templates', static_url_path="/app")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html", quote=path)


@app.route("/")
def index():
    quote = "I am the captain now!"
    return render_template("index.html", quote=quote)


@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})


@app.route('/form', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        first_name = request.form.get("fname")
        # getting input with name = lname in HTML form
        last_name = request.form.get("lname")
        return f"Your name is {first_name.title()} {last_name.title()}"
    return render_template("form.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
