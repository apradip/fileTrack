from flask import Flask, request, jsonify, make_response, escape
from flask_restful import reqparse, abort, Api, Resource
# from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# import requests
import os
import random as random
import ssl
import smtplib
from email.message import EmailMessage


def generateOtp(length):
    otp = ""

    try:
        for i in range(length):
            otp += str(random.randint(0, 9))

        return otp
    except Exception as e:
        raise Exception(e)


def sendEmail(receiver, subject, body):
    message = 'Subject: {}\n\n{}'.format(subject, body)

    try:
        server = smtplib.SMTP_SSL(os.environ.get(
            'FT_SMTP_SERVER'), os.environ.get('FT_SMTP_PORT'))
        server.login(os.environ.get('FT_SMTP_USER'),
                     os.environ.get('FT_SMTP_PASSWORD'))
        server.sendmail(os.environ.get('FT_SMTP_USER'), receiver, message)
        server.close()

    except Exception as e:
        raise Exception(e)


def sendSms(receiver, body):
    try:
        parameters = {'authkey': os.environ.get('FT_SMS_API_KEY'),
                      'receiver': receiver,
                      'payload': body,
                      'launch_datetime': ''}

        response = requests.get(url=os.environ.get(
            'FT_SMS_URL'), params=parameters)

        data = response.json()
    except Exception as e:
        raise Exception(e)
