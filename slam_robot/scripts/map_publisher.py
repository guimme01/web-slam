#!/usr/bin/python3

import rospy
from nav_msgs.msg import OccupancyGrid

def map_callback(data):
    rospy.loginfo(f"Map updated")
    publish_map(data)

def publish_map(map):
    map_pub = rospy.Publisher('/gmap', OccupancyGrid, queue_size=10)
    map_pub.publish(map)

def main():
    rospy.init_node('map_subscriber', anonymous=True)
    rospy.Subscriber('/map', OccupancyGrid, map_callback)
    rospy.spin()

if __name__ == '__main__':
    main()