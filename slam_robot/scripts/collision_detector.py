#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from slam_robot.msg import backward_collision
from slam_robot.msg import slam_robot_control
import math

ROBOT_WIDTH_X = 1  # base_link_x_dim
SAFE_DISTANCE = 3  # Minimum safe distance from obstacles (meters)

THRESHOLD = (ROBOT_WIDTH_X / 2) + SAFE_DISTANCE  # / 2 because the lidar is at the center-top of the robot

pub = rospy.Publisher('/backward_collision', backward_collision, queue_size=10)
pub_control = rospy.Publisher('/robot_commands', slam_robot_control, queue_size=10)

stopped = False

def publish_msg(distance, position):
    global stopped
    msg = backward_collision()
    msg.distance = distance
    msg.position = position

    if distance > 2.5:
        msg.dangerous_level = 1  # Low danger
    elif distance > 2 and distance <= 2.5:
        msg.dangerous_level = 2  # Medium danger
    elif distance > 1.2 and distance <= 2:
        msg.dangerous_level = 3  # High danger
        stopped = False
    else:
        msg.dangerous_level = 4  # Imminent collision
        control = slam_robot_control()
        control.direction = "stop"
        control.backward = False
        #rospy.logwarn(f"Obstacle detected, stopping. Direction: {position}")
        if(stopped):
            pass
        else:
            pub_control.publish(control)
            stopped = True
    pub.publish(msg)

def get_obstacle_direction(angle):
    if 90 < angle <= 110:
        return "left"
    elif -180 <= angle <= -160:
        return "right"
    else:
        return "back"

def lidar_callback(data):
    angle_min = data.angle_min
    angle_increment = data.angle_increment

    min_distance = float('inf')
    closest_angle = None

    for i, distance in enumerate(data.ranges):
        angle = angle_min + i * angle_increment
        if 90 < abs(math.degrees(angle)) <= 180:
            if distance > 0 and distance != float('inf') and distance < min_distance:
                min_distance = distance
                closest_angle = angle

    if min_distance < THRESHOLD and closest_angle is not None:
        direction = get_obstacle_direction(math.degrees(closest_angle))
        rospy.logwarn(f"Obstacle detected at {min_distance} meters, direction: {direction}!")
        publish_msg(min_distance, direction)

def main():
    rospy.init_node('lidar_backward_collision', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, lidar_callback)
    rospy.loginfo("Backward collision detection node started.")
    rospy.spin()

if __name__ == "__main__":
    main()