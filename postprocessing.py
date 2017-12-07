import time

def convert_to_datetime(created_at):
    return time.strftime('%Y-%m-%d', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))