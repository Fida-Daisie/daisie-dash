
from flask import request
import json
import requests
from flask import redirect, request
from ..core.misc import  config_reader
from ..core.authentification.User import User
from flask_login import login_user

def oauth_routes(daisie_main):
    config = config_reader().get_config()
    callback_url = config['oauth'].get('callback_url')
    base_url = config['url'].get('base_url')
    server = daisie_main.server
    @server.route('/login')
    def login():
        open_id = config['oauth'].get('openid_configuration')
        provider_cfg=requests.get(open_id).json()
        authorization_endpoint = provider_cfg["authorization_endpoint"]
        request_uri = daisie_main.client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=base_url+callback_url,
        scope=["openid", "email", "profile"],
        )
        
        return redirect(request_uri)
    



    @server.route(callback_url)
    def callback():
        # Get authorization code provider sent back to you
        code = request.args.get("code")
        config = config_reader().get_config()
        open_id = config['oauth'].get('openid_configuration')
        provider_cfg = requests.get(open_id).json()
        token_endpoint = provider_cfg["token_endpoint"]
        token_url, headers, body = daisie_main.client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
        )
        
        client_id = config['oauth'].get('client_id')
        client_secret = config['oauth'].get('client_secret')
        token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(client_id, client_secret),
        
            )

        # Parse the tokens!
        daisie_main.client.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = provider_cfg["userinfo_endpoint"]
        uri, headers, body = daisie_main.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            users_name = userinfo_response.json()["given_name"]
        else:
            return "User email not available or not verified by the Oauth provider.", 400
        user = User(
        id=unique_id, name=users_name, email=users_email
        )

        # Doesn't exist? Add it to the database.
        if not User.get(unique_id):
            User.create(unique_id, users_name, users_email)

        # Begin user session by logging the user in
        login_user(user)

        # Send user back to homepage
        
        return redirect("/report")