import json
import datetime
import time
import os
import dateutil.parser
import logging
import boto3

s3 = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# --- Helpers that build all of the responses ---


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


# --- Helper Functions ---


def safe_int(n):
    """
    Safely convert n value to int.
    """
    if n is not None:
        return int(n)
    return n


def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None

def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

def isvalid_feeling(feeling):
    feelings = ['bad', 'suicidal', 'anxious', 'depressed', 'good']
    return feeling.lower() in feelings

def feeling(intent_request):
    slots = intent_request['currentIntent']['slots']
    feeling = slots['Feeling']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    if feeling and not isvalid_feeling(feeling):
        return build_validation_result(
            False,
            'Feeling',
            'We currently do not support {}.  Can you try a different feeling?'.format(feeling)
        )
    
    if feeling == 'Bad':
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': 'I\'m sorry you are feeling bad :('
            }
        )
        
    elif feeling == 'Good':
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': 'I\'m glad you are feeling good! :)'
            }
        )
        
    elif feeling == 'Suicidal':
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': 'Oh no! Lets get you help right away. Here is a suicide prevention hotline 1-800-273-8255'
            }
        )
   
    elif feeling == 'Anxious':
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': 'I\'m sorry you are feeling anxious. If you would like to talk to someone about it, here is a anxiety hotline: 1-800-950-6264'
            }
        )
        
    elif feeling == 'Depressed':
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': 'I\'m sorry you are feeling depressed. If you would like to talk to find treatment, here is a treatment locator: 1-800-662-4357'
            }
        )
    
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Please try again and capitalize your feeling this time'
        }
    )

def isvalid_med(med):
    meds = ['prozac', 'wellbutrin', 'zoloft']
    return med.lower() in meds

def medication(intent_request):
    slots = intent_request['currentIntent']['slots']
    med = slots['Meds']
    info = slots['Info_Desired']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    bucket = 'cmsc389l-healthbot'

    if med and not isvalid_med(med):
        return build_validation_result(
            False,
            'Meds',
            'We currently do not support {}.  Can you try a different Medication?'.format(med)
        )
    
    if info == 'info' or info == 'Info':
        if med == 'Prozac' or med == 'prozac':
            key = 'prozac_info.txt'
            data = s3.get_object(Bucket=bucket, Key=key)
            json_data = data['Body'].read()
            return close(
                session_attributes,
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': json_data
                }
            )
            
        elif med == 'Wellbutrin' or med == 'wellbutrin':
            key = 'wellbutrin_info.txt'
            data = s3.get_object(Bucket=bucket, Key=key)
            json_data = data['Body'].read()
            return close(
                session_attributes,
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': json_data
                }
            )

        elif med == 'Zoloft' or med == 'zoloft':
            key = 'zoloft_info.txt'
            data = s3.get_object(Bucket=bucket, Key=key)
            json_data = data['Body'].read()
            
            return close(
                session_attributes,
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': json_data
                }
            )
    elif info == "Comparison" or info == "comparison":
        key = 'comparison.txt'
        data = s3.get_object(Bucket=bucket, Key=key)
        json_data = data['Body'].read()
            
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': json_data
            }
        )
            
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'no match'
        }
    )
# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    print("in dispatch")

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'IWantToTalk':
        return feeling(intent_request)
    elif intent_name == 'Medication':
        return medication(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    
    return dispatch(event)
