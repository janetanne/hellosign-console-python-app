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
                 10: "send non-embedded sig request with file_url NOT USING SDK",
                 11: "list signature requests",
                 12: "send embedded signature request",
                 13: "send embedded signature request with template",
                 14: "get files of signature request",
                 0 : "exit app",
                }

def run_app():
    '''Runs the console app.'''
    
    print("\n\nWelcome to Janet's HelloSign Console App!\n\n")

    while True:
        
        print_menu()
        user_choice = return_choice()
        
        if user_choice == 0:
            break

        process_choice(user_choice)

def print_menu():
    '''Takes in no argument, prints the menu list'''
        
    for k, v in MENU_CHOICES.items():
        pprint("Type {} to {}".format(k, v))

def return_choice():
    '''Takes in no argument, returns integer. If the input given is not an integer, loops until input is an integer.'''

    while True:

        try:
            choice = int(input("What would you like to do today? >>"))

        except ValueError:
            pprint("Oops! Looks like you entered something that wasn't a number. Try again?")
            continue

        else:
            return choice
            break

def process_choice(num):
    
    signers = [
                    { "name": "JANET PERSONAL",
                      "email_address" : "janetpanen@gmail.com",
                    #   "role_name" : "Client"
                    },
                    # { "name" : "JANET DBX",
                    #  "email_address": "janet.anne@dropbox.com"
                    # },
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
        pprint("This has been sent to your signers. Check your email!")

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
                                        client_id=CLIENT_ID
        )
    
    # send non-embedded sig request with template & custom fields
    elif num == 4:
        templ_id = input("Please provide the template id for sending out a signature request >> ")
        custom_fields = [
                            {"test_1" : "value for test_1" },
                            {"test_2" : "value for test_2" }
        ]

        signature_request = client.send_signature_request_with_template(
                                        template_id=templ_id,
                                        signers=signers,
                                        client_id=CLIENT_ID,
                                        custom_fields=custom_fields,
        )

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
    
    # sends a non-embbeded sig request NOT USING THE SDK
    elif num == 9:

        buildTheRequest = 'https://' + API_KEY + \
                          ':@api.hellosign.com/v3/signature_request/send'
   
        data = {
            'client_id': CLIENT_ID,
            # 'template_id': '0e9e8276e97b9cc93694058cf6eb6e8b1975cd0a',
            'subject': 'test with console - no SDK',
            # 'message': 'test',
            'signers[0][name]': 'George',
            'signers[0][email_address]': 'janetanne@dropbox.com',
            'test_mode': '1',
            'file[0]': files,
            'field_options': {"date_format":"DD - MM - YYYY"},
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
            # 'template_id': '0e9e8276e97b9cc93694058cf6eb6e8b1975cd0a',
            # 'file[0]' : 'test', # NEED TO GET A PUBLIC URL THROUGH AWS
            'subject': 'test',
            'message': 'test',
            'signers[Client][name]': 'George',
            'signers[Client][email_address]': 'janet.anne@hellosign.com',
            'test_mode': '1'
        }

        print(buildTheRequest)
        r = requests.post(buildTheRequest, data)
        print(r.text)
    
    # lists signature requests
    elif num == 11:
        signature_request_list = client.get_signature_request_list(page=1)

        for signature_request in signature_request_list:
            pprint("signature_request_id: {}, signature_request_status: {}".format(
                signature_request.signature_request_id, signature_request.is_complete)
        
    # "send embedded signature request",
    elif num == 12: 
        signature_request = client.send_signature_request_embedded(
            test_mode = 1,
            client_id = CLIENT_ID,
            files = files,
            subject = "EMBEDDED SIGNATURE REQUEST VIA CONSOLE APP",
            message = "test test test test",
            signing_redirect_url = None,
            signers = signers,
        )
        for signature in signature_request.signatures:
            embedded_obj = client.get_embedded_object(signature.signature_id)
            sign_url = embedded_obj.sign_url
            pprint(sign_url)


    # send embedded signature request with template
    elif num == 13:
        templ_id = input("Please provide the template id for sending out a signature request >> ")
        signature_request = client.send_signature_request_embedded_with_template(
            test_mode = 1,
            client_id = CLIENT_ID,
            template_id = templ_id,
            subject = "EMBEDDED SIGNATURE REQUEST VIA CONSOLE APP",
            message = "test test test test",
            signing_redirect_url = None,
            signers = [ 
                        { "role_name" : "Client",
                          "email_address" : "janetpanen@gmail.com",
                          "name" : "JANET PERSONAL"
                        }
                       ],
        )
        for signature in signature_request.signatures:
            embedded_obj = client.get_embedded_object(signature.signature_id)
            sign_url = embedded_obj.sign_url
            pprint(sign_url)

    elif num == 14:
        sig_req_id = input("Please provide the signature request files you'd like to download >> ")
        url = self.SIGNATURE_REQUEST_DOWNLOAD_PDF_URL + sig_req_id
        return request.get(self)


    else:
        pprint("This was not a valid choice, please choose an option in the list.")
        return_choice()


if __name__ == "__main__":
      run_app()  





