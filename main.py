from pprint import pprint
from hellosign_sdk import HSClient
import os
import requests
import json

API_KEY = os.environ['API_KEY']
CLIENT_ID = os.environ['CLIENT_ID']

client = HSClient(api_key=API_KEY)


MENU_CHOICES = { 1 : "send non-embedded signature request",
                 2 : "get signature request",
                 3 : "send non-embedded signature request with template",
                 4 : "send non-embedded signature request with template & custom fields",
                 5 : "cancel signature request",
                 6 : "send a reminder for signature request",
                 7 : "get account info",
                 8 : "get template",
                 9 : "send non-embedded signature request with template NOT USING SDK",
                 10: "sends non-embedded sig request with file_url NOT USING SDK",
                 11: "list signature requests",
                 0 : "exit app",
                }

def run_app():
    
    pprint("\n\nWelcome to Janet's HelloSign Console App!\n\n")
    
    running = True

    while running:
        
        print_menu()
        choice = return_choice()
        process_choice(choice)
        
        if process_choice == 0:
                running = False

    # NEED TO FIX THIS LOOP; DOESN'T ACTUALLY LET ME EXIT

def print_menu():
        
    for k, v in MENU_CHOICES.items():
        pprint("Type {} to {}".format(k, v))

def return_choice():

    choice = int(input("What would you like to do today? >>"))

    return choice

def process_choice(num):
    
    signers = [
                    { "name": "Janet",
                      "email_address" : "janet.anne@dropbox.com"},
                    # { "name" : "Janet 2",
                    #  "email_address": "janetpanen@gmail.com" }
                ]
    files = ["blank_test.pdf"]
    
    # send non-embedded signature request
    if num == 1:
        
        signature_request = client.send_signature_request(
                                                files=files,
                                                title="TEST VIA CONSOLE APP",
                                                subject="console app testing",
                                                signers=signers
                                                )

    # get signature request
    elif num == 2:
        sig_req_id = input("Please provide the signature request id >> ")
        signature_request = client.get_signature_request(sig_req_id)
        pprint("This is the requester email address: {} for signature request \
                id {}".format(signature_request.requester_email_address, \
                        signature_request.signature_request_id))
    
    # send non-embedded sig request with template
    elif num == 3:
        templ_id = input("Please provide the template id for sending out a signature request >> ")
        signature_request = client.send_signature_request_with_template(
                                        template_id=templ_id,
                                        title="TEMPLATE TEST VIA CONSOLE APP",
                                        subject="template test via console app",
                                        signers=signers,
        )
    
    # TO DO: send non-embedded sig request with template & custom fields
    elif num == 4:
            pass

    # cancel signature request
    elif num == 5:
        sig_id = input("Please provide the signature id >> ")
        client.cancel_signature_request(sig_id)
        pprint("Signature request {} has been cancelled".format(sig_id))

    # send reminder for signature request
    elif num == 6:
        sig_req_id = input("Please provide the signature request id of the signer >> ")
        signer_email = input("Please provide the email address of the signer you want to remind >> ")
        client.remind_signature_request(sig_req_id, signer_email)
        pprint("Reminder for signature request {} has been sent to {}".format(sig_req_id, signer_email))


    # get account info
    elif num == 7:
            account = client.get_account_info()
            pprint("This is the email address associated with this account: {}".format(account.email_address))

    # get template
    elif num == 8:
            templ_id = input("Please provide the template id >> ")
            templ = client.get_template(templ_id)
            pprint("Accounts that can access this template: {}".format(templ.accounts))
    
    # sends a non-embbeded sig request with template NOT USING THE SDK
    elif num == 9:

        buildTheRequest = 'https://' + API_KEY + \
                          ':@api.hellosign.com/v3/signature_request/send_with_template'
   
        data = {
            'client_id': CLIENT_ID,
            'template_id': '0e9e8276e97b9cc93694058cf6eb6e8b1975cd0a',
            'subject': 'test',
            'message': 'test',
            'signers[Client][name]': 'George',
            'signers[Client][email_address]': 'alex.mcferron@hellosign.com',
            'test_mode': '1'
        }

        print(buildTheRequest)
        r = requests.post(buildTheRequest, data)
        print(r.text)
        # Collapse

    # sends non-embedded sig request with file_url
    elif num == 10:
        buildTheRequest = 'https://' + API_KEY + \
                          ':@api.hellosign.com/v3/signature_request/send'
   
        data = {
            'client_id': CLIENT_ID,
            'template_id': '0e9e8276e97b9cc93694058cf6eb6e8b1975cd0a',
            'subject': 'test',
            'message': 'test',
            'signers[Client][name]': 'George',
            'signers[Client][email_address]': 'janet.anne@hellosign.com',
            'test_mode': '1'
        }

        print(buildTheRequest)
        r = requests.post(buildTheRequest, data)
        print(r.text)
    
    elif num == 11:
        signature_request_list = client.get_signature_request_list(page=1)
        pprint(signature_request_list)

    elif num == 0:
        running = False
        return running

    else:
        new_choice = input("Seems like you've chosen an invalid option. Try again, or type 0 to exit >> ")
        return new_choice

if __name__ == "__main__":
      run_app()  





