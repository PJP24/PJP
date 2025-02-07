from authlib.integrations.starlette_client import OAuth
from starlette.config import Config


config = Config('orchestrator_monolith/src/orchestrator/.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
google = oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


github = oauth.register(
    name="github",
    client_id=config.get("GITHUB_CLIENT_ID"),
    client_secret=config.get("GITHUB_CLIENT_SECRET"),
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)