import math
deg2rad = math.pi/180
rad2deg = 180/math.pi

def cartesian_x(f,l):
    #f = latitude, l = longitude
    return (math.cos(f*deg2rad)*math.cos(l*deg2rad))

def cartesian_y(f,l):
    #f = latitude, l = longitude
    return (math.cos(f*deg2rad)*math.sin(l*deg2rad))

def cartesian_z(f,l):
    #f = latitude, l = longitude
    return (math.sin(f*deg2rad))

def spherical_lat(x,y,z):
    r = math.sqrt(x*x + y*y)
    #Omitting the special cases because points will always 
    #be separated for this application
    return (math.atan2(z, r)*rad2deg) # return degrees
    
def spherical_lng(x,y,z):
    #Omitting the special cases because points will always 
    #be separated for this application
    return (math.atan2(y, x)*rad2deg) # return degrees

def midpoint_lat(f0,l0, f1,l1):
    #get the x y and z values
    x_0 = cartesian_x(f0,l0)
    y_0 = cartesian_y(f0,l0)
    z_0 = cartesian_z(f0,l0)
    x_1 = cartesian_x(f1,l1)
    y_1 = cartesian_y(f1,l1)
    z_1 = cartesian_z(f1,l1)
   
    x_mid = (x_0+x_1)/2
    y_mid = (y_0+y_1)/2
    z_mid = (z_0+z_1)/2

    return spherical_lat(x_mid, y_mid, z_mid)

def midpoint_lng(f0,l0, f1,l1):
    #get the x y and z values
    x_0 = cartesian_x(f0,l0)
    y_0 = cartesian_y(f0,l0)
    z_0 = cartesian_z(f0,l0)
    x_1 = cartesian_x(f1,l1)
    y_1 = cartesian_y(f1,l1)
    z_1 = cartesian_z(f1,l1)
   
    x_mid = (x_0+x_1)/2
    y_mid = (y_0+y_1)/2
    z_mid = (z_0+z_1)/2

    return spherical_lng(x_mid, y_mid, z_mid)

#half_lat = midpoint_lat(37.72286,-122.42299, 41.0625,-112.0417)
#half_lng = midpoint_lng(37.72286,-122.42299, 41.0625,-112.0417)

#print(str(half_lat) + "," + str(half_lng))