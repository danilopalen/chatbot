from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def index():
    import collections
    import json
    from ibm_watson import AssistantV2
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    # my bot
    my_apikey = 'YOL8n5EcRf2D1b8YrkT6ATix7o5TdcwNso5wYtXY2wIi'
    my_aid = '9097fa59-e0fa-4bad-b0e6-195f76bae232'
    my_url = 'https://api.au-syd.assistant.watson.cloud.ibm.com/instances/5acee416-015c-42ea-9ba1-e8549214ef5c'

    authenticator = IAMAuthenticator(my_apikey)
    assistant = AssistantV2(
        version='2020-04-01',
        authenticator=authenticator
    )

    assistant.set_service_url(my_url)

    session = assistant.create_session(
        assistant_id = my_aid
    ).get_result()

    if request.method == 'POST':
        user_input = request.form['input']
    else:
        user_input = ''

    response = assistant.message(
        assistant_id = my_aid,
        session_id = session['session_id'], 
        input={
            'message_type': 'text',
            'text': user_input            
        }
    ).get_result()

    print(json.dumps(response, indent=2))

    results = response['output']['generic'][0]['text']    
    options = []
 
    for item in response['output']['generic']:
        if 'options' in item:
            options = response['output']['generic'][1]['options']
            
    return render_template("home.html", results = results, options = options)


   

    