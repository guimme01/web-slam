#!/usr/bin/python3

import rospy
import os
from slam_robot.srv import create_map, create_mapResponse

def create_map_service(req):
    map_name = req.map_name
    maps_directory = '/home/guimme/catkin_ws/src/slam_robot/maps'

    try:
        if not os.path.exists(maps_directory):
            os.makedirs(maps_directory)

        yaml_file_path = os.path.join(maps_directory, f'{map_name}')

        os.system(f"rosrun map_server map_saver -f {yaml_file_path}")


        return create_mapResponse(success=True)

    except Exception as e:

        rospy.logerr(f"Errore nella creazione della mappa: {str(e)}")
        return create_mapResponse(success=False)

def map_creator_server():
    rospy.init_node('create_map_server')

    s = rospy.Service('create_map', create_map, create_map_service)
    rospy.loginfo("Servizio 'create_map' pronto.")
    rospy.spin()

if __name__ == '__main__':
    try:
        map_creator_server()
    except rospy.ROSInterruptException:
        pass
