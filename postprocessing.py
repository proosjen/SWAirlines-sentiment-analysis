import time

'''
This function converts the created_at date
we collected from the Twitter streaming API
into a Python datetime object.
'''
def convert_to_datetime(created_at):
    return time.strftime('%Y-%m-%d', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))