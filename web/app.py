from flask import Flask, request
from beans.contributions import Contribution
from client.sheets import GoogleSheetsClient
from client.twilio import TwilioClient
from service.sheets import ContributionsSheetsService
from flask_api import status
from util.text_table import TextTableUtil
import logging
from datetime import datetime, timezone
import pytz
from flask import render_template
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
google_sheets_client = GoogleSheetsClient()
contributions_sheet_service = ContributionsSheetsService(google_sheets_client)
twilio_client = TwilioClient()

@app.route("/")
def index():
    return render_template(template_name_or_list="index.html")

@app.route("/contributions/add",  methods = ['GET', 'POST'])
def add_contribution():
    if request.method == 'GET':
        return render_template(template_name_or_list="add_new_contribution.html")

    if request.method == 'POST':
        name = request.form.get("name")
        amount = request.form.get("amount")

        if not name or not amount:
            return render_template(
                template_name_or_list="add_new_contribution.html", 
                message="Name or amount is not entered", 
                status="Failure"
            )

        contribution_json = json.loads('{"name": "%s", "amount": "%s"}' % (name, amount))
        contribution = Contribution(contribution_json)
        logging.info("Adding contribution with name %s and amount Rs. %s" % (
            contribution.name, str(contribution.amount)))
        contributions_sheet_service.add_new_contribution(contribution)

        return render_template(template_name_or_list="add_new_contribution.html", message="Contribution added successfully!", status="Success")

@app.route("/contributions/get/<channel>")
def get_contributions(channel):
    logging.info("Logging contributions to channel %s" % channel)
    contributions = contributions_sheet_service.get_all_contributions()
    text_table = TextTableUtil.build_text_table_from_contributions(contributions, use_texttable=channel=='console', use_html=channel=='web')
    current_time = get_current_datetime()
    message = "Murti Collection(2022) as of %s \n\n%s\n\n" % (current_time, text_table)
    
    if channel == 'whatsapp':
        sid = twilio_client.send_message(body=message)
        logging.info("Message sent on whatsapp, sid=%s" % sid)
    elif channel == 'console':
        logging.info("\n" + message)
    elif channel == 'web':
        html_message_format = "<div class='container'>%s</div>"
        return render_template(
                template_name_or_list="view_contributions.html", 
                message=html_message_format % message
            )
    else:
        return '{"status": "Failure", "message": "Channel %s not supported!"}' % channel, status.HTTP_400_BAD_REQUEST

    return '{"status": "Success", "message": "Contributions logged to channel, %s!"}' % channel

def get_current_datetime():
    tz = pytz.timezone('Asia/Kolkata')
    return str(datetime.now(tz).strftime("%a %d %B, %Y %H:%M:%S"))

if __name__ == '__main__':
    app.run()
