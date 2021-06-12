from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "wt3xcNU-JXTRgFZpBVA5CEI78M4uOO-5PViTN-P6T3rXCog-UZpS8Ts5lw3shULA4gQeprnlREfCwQ71j2Y1XA=="
org = "alan.mangroo@gmail.com"
bucket = "Temperatures"

client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

data = "mem,host=host1 used_percent=23.43234543"
write_api.write(bucket, org, data)
