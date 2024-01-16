import numpy
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

def cross_x(x, y, z, i,j,k):
    return ((y*k)-(z*j))
def cross_y(x, y, z, i,j,k):
    return ((z*i)-(x*k))
def cross_z(x, y, z, i,j,k):
    return ((x*j)-(y*i))

def spherical_lat(x,y,z):
    r = math.sqrt(x*x + y*y)
    #Omitting the special cases because points will always
    #be separated for this application
    return (math.atan2(z, r)*rad2deg) # return degrees

def spherical_lng(x,y,z):
    #Omitting the special cases because points will always
    #be separated for this application
    return (math.atan2(y, x)*rad2deg) # return degrees


#lat, lng for tx
t_lat = 37.7248952200944
t_lng = -122.422936174405
#lat,lng for rx
r_lat = 51.9561076
r_lng = 5.2400448
#lat,lng for ionosonde
c_lat = 45.07
c_lng = -83.56


tx_x = cartesian_x(t_lat,t_lng)
tx_y = cartesian_y(t_lat,t_lng)
tx_z = cartesian_z(t_lat,t_lng)
rx_x = cartesian_x(r_lat,r_lng)
rx_y = cartesian_y(r_lat,r_lng)
rx_z = cartesian_z(r_lat,r_lng)
c_x = cartesian_x(c_lat,c_lng)
c_y = cartesian_y(c_lat,c_lng)
c_z = cartesian_z(c_lat,c_lng)

#The plane containing the path
g_x = cross_x(tx_x, tx_y, tx_z, rx_x, rx_y, rx_z)
g_y = cross_y(tx_x, tx_y, tx_z, rx_x, rx_y, rx_z)
g_z = cross_z(tx_x, tx_y, tx_z, rx_x, rx_y, rx_z)
#The plane containing the ionosonde and perpendicular to the path?
f_x = cross_x(c_x, c_y, c_z, g_x, g_y, g_z)
f_y = cross_y(c_x, c_y, c_z, g_x, g_y, g_z)
f_z = cross_z(c_x, c_y, c_z, g_x, g_y, g_z)
t_x = cross_x(g_x, g_y, g_z, f_x, f_y, f_z)
t_y = cross_y(g_x, g_y, g_z, f_x, f_y, f_z)
t_z = cross_z(g_x, g_y, g_z, f_x, f_y, f_z)

t_mag = math.sqrt(t_x**2 + t_y**2 + t_z**2)

tp_x = t_x/t_mag
tp_y = t_y/t_mag
tp_z = t_z/t_mag

print("stations and ionosonde")
line3d(numpy.array([(0,0,0), (tx_x,tx_y,tx_z)]))+line3d(numpy.array([(0,0,0), (rx_x,rx_y,rx_z)]))+line3d(numpy.array([(0,0,0), (c_x,c_y,c_z)]),color='purple')
print("g: plane of the path")
line3d(numpy.array([(0,0,0), (tx_x,tx_y,tx_z)]))+line3d(numpy.array([(0,0,0), (rx_x,rx_y,rx_z)]))+line3d(numpy.array([(0,0,0), (c_x,c_y,c_z)]), color='purple')+line3d(numpy.array([(0,0,0), (g_x,g_y,g_z)]), radius=0.01, color='green')+polygon3d([[0,0,0], [tx_x,tx_y,tx_z], [rx_x,rx_y,rx_z]],color=(0,1,0), opacity=0.7)
print("f: plane of c and g")
line3d(numpy.array([(0,0,0), (tx_x,tx_y,tx_z)]))+line3d(numpy.array([(0,0,0), (rx_x,rx_y,rx_z)]))+line3d(numpy.array([(0,0,0), (c_x,c_y,c_z)]), color='purple')+line3d(numpy.array([(0,0,0), (g_x,g_y,g_z)]), radius=0.01, color='green')+line3d(numpy.array([(0,0,0), (f_x,f_y,f_z)]), radius=0.01, color='red')+polygon3d([[0,0,0], [tx_x,tx_y,tx_z], [rx_x,rx_y,rx_z]],color=(0,1,0), opacity=0.7)+polygon3d([[0,0,0], [c_x,c_y,c_z], [g_x,g_y,g_z]],color=(1,0,0), opacity=0.5)
print("t: plane of g and f")
line3d(numpy.array([(0,0,0), (tx_x,tx_y,tx_z)]))+line3d(numpy.array([(0,0,0), (rx_x,rx_y,rx_z)]))+line3d(numpy.array([(0,0,0), (c_x,c_y,c_z)]), color='purple')+line3d(numpy.array([(0,0,0), (g_x,g_y,g_z)]), radius=0.01, color='green')+line3d(numpy.array([(0,0,0), (f_x,f_y,f_z)]), radius=0.01, color='red')+line3d(numpy.array([(0,0,0), (tp_x,tp_y,tp_z)]), radius=0.01, color='black')+polygon3d([[0,0,0], [tx_x,tx_y,tx_z], [rx_x,rx_y,rx_z]],color=(0,1,0), opacity=0.7)+polygon3d([[0,0,0], [c_x,c_y,c_z], [g_x,g_y,g_z]],color=(1,0,0), opacity=0.5)+polygon3d([[0,0,0], [g_x,g_y,g_z], [f_x,f_y,f_z]],color=(1,1,0), opacity=0.3)
print("path on point lat,lng: " + str(spherical_lat(tp_x,tp_y,tp_z)) + "," + str(spherical_lng(tp_x,tp_y,tp_z)))
