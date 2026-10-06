# 0xAmanita

import os
import logging
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# no secret key set = sessions are unsigned and forgeable.
app.secret_key = "insecure-demo-key-do-not-use"

# vulnerability: plaintext credential log

LOG_FILE = os.path.join(os.path.dirname(__file__), "credentials.log")

# python's logging module here just for timestamps; the real problem
# is that we are logging the RAW PASSWORD at all.
cred_logger = logging.getLogger("credentials")
cred_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
)
cred_logger.addHandler(file_handler)

# routes

@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    message = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username or password:
            # raw password written
            cred_logger.info("USERNAME=%s | PASSWORD=%s", username, password)

        message = {
            "type": "success",
            "text": (
                'Success'
            ),
        }

    return render_template("login.html", message=message)

# entry point

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
