#!/usr/bin/env python3.11

"""Module for creating survey and sending email invitations to recipients"""

import http.client
import json
import sys
import os
from dotenv import load_dotenv

def parse_questions(questions):
    parsed_questions = []
    for item in questions.items():
        question = {}
        question["headings"] = []
        question["headings"].append({ "heading" : questions[item[0]]["Description"] })
        question["family"] = "single_choice"
        question["subtype"] = "vertical"
        question["answers"] = {}
        question["answers"]["choices"] = []
        for value in questions[item[0]]["Answers"]:
            question["answers"]["choices"].append({ "text" : value })
        parsed_questions.append(question)
    return parsed_questions

def parse_pages(pages):
    parsed_pages = []
    pos = 1
    for item in pages.items():
        parsed_pages.append( {
            "title": item[0],
            "position": pos,
            "questions": parse_questions(pages[item[0]])
            }
        )
        pos += 1
    return parsed_pages

def parse_survey_data(filename):
    with open(filename, "r", encoding="utf-8") as file:
        survey_data = json.loads(file.read())
    res = {}
    survey_name = list(survey_data.keys())[0]
    res["title"] = survey_name
    res["pages"] = parse_pages(survey_data[survey_name])
    return res

def send_post_request(uri, payload):
    load_dotenv()
    conn = http.client.HTTPSConnection("api.surveymonkey.com")
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': "Bearer " + os.getenv('token')
    }
    conn.request("POST", uri, payload, headers)
    res = conn.getresponse()
    return res.read()

def parse_email_file(filename):
    contacts_payload = {}
    contacts_payload["contacts"] = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            contacts_payload["contacts"].append({ "email": line })
    return contacts_payload

def send_email_invitations(survey_id):
    create_collector_uri = "/v3/surveys/" + survey_id + "/collectors"
    create_collector_payload = { "type": "email" }
    create_collector_response = send_post_request(create_collector_uri,
                                                  json.dumps(create_collector_payload))
    collector_id = json.loads(create_collector_response)['id']
    format_message_uri = "/v3/collectors/" + collector_id + "/messages"
    format_message_payload = { "type": "invite" }
    format_message_response = send_post_request(format_message_uri,
                                                json.dumps(format_message_payload))
    message_id = json.loads(format_message_response)['id']
    upload_recipients_uri = format_message_uri + "/" + message_id + "/recipients/bulk"
    upload_recipients_payload = json.dumps(parse_email_file(sys.argv[2]))
    send_post_request(upload_recipients_uri, upload_recipients_payload)
    send_message_uri = format_message_uri + "/" + message_id + "/send"
    send_post_request(send_message_uri, {})

if len(sys.argv) != 3:
    print ("You should provide 2 arguments: JSON with survey and list of participants mails")
    sys.exit(1)

survey_payload_dict = parse_survey_data(sys.argv[1])
survey_payload = json.dumps(survey_payload_dict)
create_survey_response = send_post_request("/v3/surveys", survey_payload)
survey_dict = json.loads(create_survey_response)
surv_id = survey_dict['id']
send_email_invitations(surv_id)
