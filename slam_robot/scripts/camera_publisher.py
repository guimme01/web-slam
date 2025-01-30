#!/usr/bin/python3

import rospy
from sensor_msgs.msg import Image

def camera_callback(data):
    rospy.loginfo(f"Camera updated")
    publish_image(data)


def publish_image(img):
    img_pub = rospy.Publisher('/camera_sens', Image, queue_size=10)
    img_pub.publish(img)

def main():
    rospy.init_node('image_raw_subscriber', anonymous=True)
    rospy.Subscriber('/image_raw', Image, camera_callback) 
    rospy.spin()

if __name__ == '__main__':
    main()
    