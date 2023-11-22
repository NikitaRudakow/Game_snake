import math

a = {"rectangle":{"left_top":{"lat":53.9219415948929,"lon":30.328681992567624},"right_bottom":{"lat":53.901415456718695,"lon":30.344775246498386}}}
def get_dist():
    lat_diff = a["rectangle"]["left_top"]["lat"] - a["rectangle"]["right_bottom"]["lat"]
    lon_diff = a["rectangle"]["left_top"]["lon"] - a["rectangle"]["right_bottom"]["lon"]
    print(math.sqrt(lon_diff * lon_diff + lat_diff * lat_diff))
get_dist()
