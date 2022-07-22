from ...misc import  config_reader


def oauth(daisie_main):
    config = config = config_reader().get_config()
    if config.has_section('google-oauth'):
        from .oauth_google import google_routes
        google_routes(daisie_main)
    if config.has_section('linkedin-oauth'):
        from .oauth_linked import linkedin_routes
        linkedin_routes(daisie_main)
    if config.has_section('github-oauth'):
        from .oauth_github import github_routes
        github_routes(daisie_main)