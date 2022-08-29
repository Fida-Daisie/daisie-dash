import json
import requests
from flask_login import login_user
from urllib.parse import urlsplit, parse_qs
from ...misc import config_reader
from ..User import User



open_id = "https://accounts.google.com/.well-known/openid-configuration"
provider_cfg = requests.get(open_id).json()


def google_routes(daisie_main, query_url:str):
    """
    DaisieMain instance and Full URL with all queries are inputs.
    """
    config = config_reader().get_config()
    base_url = config['url'].get('base_url')
    callback_url = config['google-oauth'].get('callback_url')

    # Get authorization code provider sent back to you
    token_endpoint = provider_cfg["token_endpoint"]
    authorization_response = query_url.replace("http://", "https://")
    redirect_url = (base_url+callback_url).replace("http://", "https://")
    code = parse_qs(urlsplit(base_url+query_url).query).get("code", [None])[0]

    token_url, headers, body = daisie_main.google_client.prepare_token_request(
        token_endpoint,
        authorization_response = authorization_response,
        redirect_url = redirect_url,
        code = code
    )
    
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(config['google-oauth'].get('client_id'), config['google-oauth'].get('client_secret')),
    )

    # Parse the tokens!
    daisie_main.google_client.parse_request_body_response(json.dumps(token_response.json()))
    
    userinfo_endpoint = provider_cfg["userinfo_endpoint"]
    uri, headers, body = daisie_main.google_client.add_token(userinfo_endpoint)
    
    userinfo_response = requests.get(uri, headers=headers, data=body)
    
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]

        user = User(
            id=unique_id, name=users_name, email=users_email
        )

        # Doesn't exist? Add it to the database.
        if not User.get(unique_id):
            User.create(unique_id, users_name, users_email)

        # Begin user session by logging the user in
        login_user(user)


def create_request_url(daisie_main):
    config = config_reader().get_config()
    base_url = config['url'].get('base_url')
    callback_url = config['google-oauth'].get('callback_url')
    authorization_endpoint = provider_cfg["authorization_endpoint"]
    
    request_uri = daisie_main.google_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=base_url+callback_url,
        scope=["openid", "email", "profile"],
    )
    return request_uri