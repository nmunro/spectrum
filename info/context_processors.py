from decouple import config

def api_keys(request) -> dict[str, str]:
    return {
        "FONT_AWESOME_API_KEY": config("FONT_AWESOME_API_KEY"),
        "GOOGLE_TAG_MANAGER_API_KEY": config("GOOGLE_TAG_MANAGER_API_KEY"),
    }
