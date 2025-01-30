#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Twist
from slam_robot.msg import slam_robot_control

current_command = None
current_backward_mode = False
new_command_received = False


def command_callback(data):
    global current_command, current_backward_mode, new_command_received

    current_command = data.direction
    current_backward_mode = data.backward
    new_command_received = True

    rospy.loginfo(f"Ricevuto comando: {current_command}, {current_backward_mode}")


def move_robot():
    global current_command, current_backward_mode, new_command_received

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(20)

    twist = Twist()

    while not rospy.is_shutdown():

        velocity = rospy.get_param('/robot_velocity', 0.5)

        if new_command_received:
            new_command_received = False
            rospy.loginfo(f"Eseguendo nuovo comando con velocità: {velocity}")

            if current_command == "forward":
                twist.linear.x = velocity
                twist.angular.z = 0.0
            elif current_command == "left":
                twist.linear.x = 0.0
                twist.angular.z = velocity
            elif current_command == "right":
                twist.linear.x = 0.0
                twist.angular.z = -velocity
            elif current_command == "stop":
                if current_backward_mode:
                    rospy.loginfo("BACKWARD ON")
                    twist.linear.x = -velocity
                    twist.angular.z = 0.0
                else:
                    rospy.loginfo("BACKWARD OFF")
                    twist.linear.x = 0.0
                    twist.angular.z = 0.0
            else:
                rospy.logwarn(f"Comando non riconosciuto: {current_command}")
                twist.linear.x = 0.0
                twist.angular.z = 0.0

        pub.publish(twist)
        rate.sleep()


def main():
    global current_command

    rospy.init_node('controller', anonymous=True)

    if not rospy.has_param('/robot_velocity'):
        rospy.set_param('/robot_velocity', 0.5)

    rospy.Subscriber('/robot_commands', slam_robot_control, command_callback)

    rospy.loginfo("Controller in attesa di comandi...")
    try:
        move_robot()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()
