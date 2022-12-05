from flask import Flask, render_template

# initialize the Flask app
app = Flask(__name__)

@app.route("/hello/")
def hello():
    """
    Render a HTML template when the "/hello/" route is requested.
    """
    return render_template("hello.html")


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)

