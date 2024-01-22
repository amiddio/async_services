def clean_url(url: str) -> str:
    if not any([url.startswith('http://'), url.startswith('https://')]):
        return 'https://' + url
    else:
        return url
