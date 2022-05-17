from ...misc import  config_reader

from .oauth_google import google_routes
from .oauth_linked import linkedin_routes
from .oauth_github import github_routes

def oauth(daisie_main):
    config = config = config_reader().get_config()
    if config.has_section('google-oauth'):
        google_routes(daisie_main)
    if config.has_section('linkedin-oauth'):
        linkedin_routes(daisie_main)
    if config.has_section('github-oauth'):
        github_routes(daisie_main)