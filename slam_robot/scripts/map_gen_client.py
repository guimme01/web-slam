#!/usr/bin/python3

import rospy
from std_msgs.msg import String
from slam_robot.srv import create_map, create_mapRequest
import rospy

def call_create_map_service(map_name):
    rospy.loginfo(f"Calling create_map service")
    rospy.wait_for_service('create_map')
    try:

        create_map_client = rospy.ServiceProxy('create_map', create_map)

        request = create_mapRequest()
        request.map_name = map_name

        response = create_map_client(request)

        if response.success:
            rospy.loginfo(f"File della mappa '{map_name}' creato correttamente.")
        else:
            rospy.logerr(f"Errore nella creazione della mappa: {response.message}")
    except rospy.ServiceException as e:
        rospy.logerr(f"Servizio create_map fallito: {e}")

def map_name_callback(msg):
    map_name = msg.data.strip()
    if map_name:
        rospy.loginfo(f"Ricevuto nome della mappa: {map_name}")
        call_create_map_service(map_name)
    else:
        rospy.logwarn("Nome della mappa non valido o vuoto.")

def main():
    rospy.init_node('map_requester_node')

    rospy.Subscriber('/map_command', String, map_name_callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
