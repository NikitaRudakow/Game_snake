# import math
#
# a ={"rectangle":{"left_top":{"lat":55.75674115376498,"lon":37.61576658138955},"right_bottom":{"lat":55.755768064218046,"lon":37.616565200673676}}}
# def get_dist():
#     lat_diff = a["rectangle"]["left_top"]["lat"] - a["rectangle"]["right_bottom"]["lat"]
#     lon_diff = a["rectangle"]["left_top"]["lon"] - a["rectangle"]["right_bottom"]["lon"]
#     print(math.sqrt(lon_diff * lon_diff + lat_diff * lat_diff))
# get_dist()
#
#
#
#



def get_square(a, b):
    return a * b, 123, "123", True

s, r, q, a = get_square(1, 2)
print(s, r, q, a)




