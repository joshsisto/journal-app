import datetime

def get_now():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def get_today():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def get_log_dir_for_today():
    return f"./logs/{datetime.datetime.now().strftime('%Y-%m-%d')}"
