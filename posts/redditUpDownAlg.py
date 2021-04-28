from datetime import datetime, timedelta, timezone
from math import log, sqrt
import pytz



# adapted from
# https://github.com/reddit-archive/reddit/blob/master/r2/r2/lib/db/_sorts.pyx
epoch = datetime(1970, 1, 1)
east_coast = pytz.timezone("America/New_York")
epoch = east_coast.localize(epoch)


print("timezone:")
print(epoch.tzinfo)
print()

def __epoch_seconds(date):
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def __score(ups, downs):
    return ups - downs

def _confidence(ups, downs):
    n = ups + downs

    if n == 0:
        return 0

    z = 1.281551565545 # 80% confidence
    p = float(ups) / n

    left = p + 1/(2*n)*z*z
    right = z*sqrt(p*(1-p)/n + z*z/(4*n*n))
    under = 1+1/n*z*z

    return (left - right) / under

# Assigns score based on upvotes, downvotes, and date posted
def hot(ups, downs, date):
    s = __score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = __epoch_seconds(date) - 1134028003
    return round(sign * order + seconds / 45000, 7)

# Assigns 'controversy score' based on upvotes and downvotes
def controversy(ups, downs):
    if downs <= 0 or ups <= 0:
        return 0

    magnitude = ups + downs
    balance = float(downs) / ups if ups > downs else float(ups) / downs

    return magnitude ** balance


# Assigns 'confidence score' based on upvotes and downvotes
# https://www.evanmiller.org/how-not-to-sort-by-average-rating.html
def confidence(ups, downs):
    up_range = 400
    down_range = 100 #these numbers were in the original reddit code
    if ups + downs == 0:
        return 0

    elif ups < up_range and downs < down_range:
        return _confidences[downs + ups * down_range]
    else:
        return _confidence(ups, downs)
