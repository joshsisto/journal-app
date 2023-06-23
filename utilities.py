import datetime

def get_now():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def get_today():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def get_log_dir_for_today():
    return f"./logs/{datetime.datetime.now().strftime('%Y-%m-%d')}"

def bold(text):
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    return bold_start + text + bold_end

def blue(text):
    blue_start = "\033[34m"
    blue_end = "\033[0m"
    return blue_start + text + blue_end

def red(text):
    red_start = "\033[31m"
    red_end = "\033[0m"
    return red_start + text + red_end