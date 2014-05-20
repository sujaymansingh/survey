"""
"""
import datetime
import json
import uuid

import flask
import boto.s3.connection as s3
from werkzeug.contrib.fixers import ProxyFix


app = flask.Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        return record_answers()

    questions = [
        {
            "text": "Are you aware of the origins and inception of the NHS in the UK?",
            "name": "1_origins",
        },
        {
            "text": "Are you aware of the contribution of immigrant medical personel involved in the provision of medical services of the NHS?",
            "name": "2_contribution",
        },
        {
            "text": "Would you like to know more about the role of immigrant medical personel in the NHS?",
            "name": "3_know_more",
        },
        {
            "text": "In which way would you like to have more information?",
            "is_label": True,
        },
        {
            "text": "1. Seminars and public meetings?",
            "name": "4_seminars",
        },
        {
            "text": "2. Websites/Internet information",
            "name": "5_websites",
        },
        {
            "text": "3. Video/Film documentary",
            "name": "6_video_film",
        },
        {
            "text": "4. Local radio station presentations",
            "name": "7_local_radio",
        },
        {
            "text": "5. All of the above",
            "name": "8_all_above",
        },
    ]

    return flask.render_template("index.html", questions=questions)


@app.route("/thank-you")
def thank_you():
    return flask.render_template("thank_you.html")


def record_answers():
    survey_response = {}

    for item in flask.request.form:
        survey_response[item] = flask.request.form[item]

    survey_response["remote_addr"] = flask.request.remote_addr
    survey_response["datetime_utc"] = datetime.datetime.utcnow().isoformat()

    conn = s3.S3Connection()
    bucket = conn.get_bucket("chaupaluk_survey", validate=False)

    key = bucket.new_key(key_name=uuid.uuid4().hex)
    key.set_contents_from_string(json.dumps(survey_response, sort_keys=True, indent=4))
    key.set_acl("public-read")
    key.close()

    return flask.redirect(flask.url_for("thank_you"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
