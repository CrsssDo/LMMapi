from datetime import datetime


def generate_code():
    timestamp = int(datetime.now().timestamp() * 1000000)
    return timestamp
