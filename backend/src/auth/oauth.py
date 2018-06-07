import json
from src.app import app
from flask import redirect, request
from rauth import OAuth2Service

class OAuthSignIn(object):
    provider = None

    def __init__(self):
        self.provider_name = app.config['AUTH_PROVIDER']
        auth_config = app.config['AUTH_CONFIG']
        self.consumer_id = auth_config['client_id']
        self.consumer_secret = auth_config['client_secret']
        self.service = OAuth2Service(
            name=self.provider_name,
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=auth_config['authorize_url'],           
            access_token_url=auth_config['access_token_url'],
            base_url=auth_config['api_base_url']
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None

        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.get('/userinfo').json()
        return me.get('email', None), me.get('given_name', 'No Name')

    def get_callback_url(self):
        return app.config['REDIRECT_URI']

    @classmethod
    def get_provider(self):
        if self.provider is None:
            self.provider = OAuthSignIn()
        return self.provider
