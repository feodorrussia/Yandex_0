import datetime
datetime_string_format = '%b %d %Y, %H:%M:%S'
data = datetime.datetime(2019, 11, 11, 11, 11, 11)
datetime_string_format = '%b %d %Y, %H:%M:%S'
print(data.strftime(datetime_string_format))