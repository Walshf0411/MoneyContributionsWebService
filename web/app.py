from flask import Flask, request
from beans.contributions import Contribution
from beans.tshirt import Tshirt
from client.sheets import GoogleSheetsClient
from client.twilio import TwilioClient
from service.sheets import ContributionsSheetsService
from service.sheets import TshirtSheetService
from flask_api import status
from util.text_table import TextTableUtil
import logging
from datetime import datetime, timezone
import pytz
from flask import render_template, redirect
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
TSHIRT_COST = 200
app = Flask(__name__)
google_sheets_client = GoogleSheetsClient()
contributions_sheet_service = ContributionsSheetsService(google_sheets_client)
tshirt_sheet_service = TshirtSheetService(google_sheets_client)
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

@app.route("/tshirt/add", methods = ["GET", "POST"])
def add_new_tshirt():
    if request.method == 'GET':
        return render_template(template_name_or_list="add_new_tshirt.html")

    if request.method == 'POST':
        name = request.form.get("name")
        quantity = request.form.get("quantity")
        size = request.form.get("size")
        notes = request.form.get("notes")
        payment = request.form.get("payment")

        # TODO: accept notes and payment 
        if not name or not quantity or not size:
            return render_template(
                template_name_or_list="add_new_tshirt.html", 
                message="Name, quantity, size is not entered", 
                status="Failure"
            )
        tshirt = Tshirt([-1, name, quantity, size, notes, payment])
        logging.info("Adding tshirt with name %s, quantity %s, size %s and payment of Rs %s" % (
            tshirt.name, str(tshirt.quantity), str(tshirt.size), str(tshirt.payment)))
        tshirt_sheet_service.add_new_tshirt(tshirt)
    
    return render_template(template_name_or_list="add_new_tshirt.html", message="Tshirt added successfully!", status="Success")


@app.route("/tshirt/get/<channel>")
def get_tshirts(channel):
    logging.info("Logging tshirt to channel %s" % channel)
    tshirts = tshirt_sheet_service.get_all_tshirt()
    text_table = TextTableUtil.build_text_table_from_tshirts(
        tshirts, use_texttable=channel == 'console', use_html=channel == 'web')
    current_time = get_current_datetime()
    message = "Murti Tshirt Status(2022) as of %s \n\n%s\n\n" % (
        current_time, text_table)

    if channel == 'whatsapp':
        sid = twilio_client.send_message(body=message)
        logging.info("Message sent on whatsapp, sid=%s" % sid)
    elif channel == 'console':
        logging.info("\n" + message)
    elif channel == 'web':
        tshirt_headers = ["id", "Name", "Quantity", "Size", "Notes", "Payment", "Date"]
        return render_template(
            template_name_or_list="view_tshirts.html",
            headers=tshirt_headers,
            rows= tshirts,
            tshirt_cost=TSHIRT_COST
        )
    else:
        return '{"status": "Failure", "message": "Channel %s not supported!"}' % channel, status.HTTP_400_BAD_REQUEST

    return '{"status": "Success", "message": "Contributions logged to channel, %s!"}' % channel

@app.route("/tshirt/update/payment/<id>")
def update_payment(id):
    if not (request.args and request.args.get('payment')):
        return '{"status": "Failure", "message": "Payment is not specified"}', status.HTTP_400_BAD_REQUEST

    payment = int(request.args.get('payment'))
    tshirt_sheet_service.update_payment(int(id), payment)
    return redirect("/tshirt/get/web", code=302)


def get_current_datetime():
    tz = pytz.timezone('Asia/Kolkata')
    return str(datetime.now(tz).strftime("%a %d %B, %Y %H:%M:%S"))

if __name__ == '__main__':
    app.run()
