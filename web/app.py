from flask import Flask, request
from beans.contributions import Contribution
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

class FlaskApp:

    def __init__(self, contributions_sheet_service, twilio_client, **configs):
        self.app = Flask(__name__)
        self.__configs(**configs)
        self.__configure_endpoints()
        self.contributions_sheet_service = contributions_sheet_service
        self.twilio_client = twilio_client

    def run(self, **kwargs):
        self.app.run(**kwargs)

    def __configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def __configure_endpoints(self):
        self.__add_endpoint("/", "index", handler=self.__index)
        self.__add_endpoint("/contributions/add", "contributions.add", handler=self.__add_contribution, methods=["GET", "POST"])
        self.__add_endpoint("/contributions/get/<channel>", "contributions.get", handler=self.__get_contributions)
    
    def __index(self):
        return '<h1>Welcome to the app</h1>'

    def __add_contribution(self):
        if request.method == 'GET':
            return render_template(template_name_or_list="add_new_contribution.html")

        if request.method == 'POST':
            name = request.form.get("name")
            amount = request.form.get("amount")

            if not name or not amount:
                return render_template(template_name_or_list="add_new_contribution.html", message="Name or amount is not entered", status="Failure")

            contribution_json = json.loads('{"name": "%s", "amount": "%s"}' % (name, amount))
            contribution = Contribution(contribution_json)
            logging.info("Adding contribution with name %s and amount Rs. %s" % (contribution.name, str(contribution.amount)))
            self.contributions_sheet_service.add_new_contribution(contribution)
        
            return render_template(template_name_or_list="add_new_contribution.html", message="Contribution added successfully!", status="Success")

    def __get_contributions(self, channel):
        logging.info("Logging contributions to channel %s" % channel)
        contributions = self.contributions_sheet_service.get_all_contributions()
        text_table = TextTableUtil.build_text_table_from_contributions(contributions, use_texttable=channel=='console', use_html=channel=='web')
        current_time = self.__get_current_datetime()
        message = "Murti Collection(2022) as of %s \n\n%s\n\nThanks" % (current_time, text_table)
        
        if channel == 'whatsapp':
            sid = self.twilio_client.send_message(body=message)
            logging.info("Message sent on whatsapp, sid=%s" % sid)
        elif channel == 'console':
            logging.info("\n" + message)
        elif channel == 'web':
            html_message_format = "<div class='container'>%s</div>"
            return html_message_format % message
        else:
            return '{"status": "Failure", "message": "Channel %s not supported!"}' % channel, status.HTTP_400_BAD_REQUEST

        return '{"status": "Success", "message": "Contributions logged to channel, %s!"}' % channel

    def __add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def __get_current_datetime(self):
        tz = pytz.timezone('Asia/Kolkata')
        return str(datetime.now(tz).strftime("%a %d %B, %Y %H:%M:%S"))