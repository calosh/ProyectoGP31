'''
import time
millis = int(round(time.time() * 1000))
print round(time.time())
print millis


from time import gmtime, strftime
print strftime("%Y-%m-%d %H:%M:%S", gmtime())

import datetime
#from datetime import datetime

# '%f' formatter reads the microseconds
a = datetime.datetime.strptime('2016-12-20 09:38:42', "%Y-%m-%d %H:%M:%S")

print(a.datetime.timestamp() * 1000)  # Unix timestamp in milliseconds

'''

import datetime

# '%f' formatter reads the microseconds
a = datetime.datetime.strptime('20.12.2016 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f')

print(a.timestamp() * 1000)  # Unix timestamp in milliseconds