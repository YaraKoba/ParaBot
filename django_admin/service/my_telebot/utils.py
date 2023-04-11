def extract_user_data_from_message(message):
    """ python-telegram-bot's Update instance --> User info """
    if message is not None:
        user = message.from_user
    else:
        raise Exception(f"Can't extract user data from update: {message}")

    return dict(
        user_id=user["id"],
        is_blocked_bot=False,
        **{
            k: user[k]
            for k in ["username", "first_name", "last_name", "language_code"]
            if k in user and user[k] is not None
        },
    )