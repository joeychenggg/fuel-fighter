#!/usr/bin/env python
import rospy
import cv2 as cv

from std_msgs import Header
from queue import Queue
from nav_msgs.msg import OccupancyGrid


from OcGrid2Jpg import map_to_matrix, matrix_to_map

PUBLISH_FREQUENCY = 1


"""
ROS subscriber and publisher object

Node: /OcGridModific
Subscribes to topic: /slam_map 
Publishes to topics: /filtered_map <- THE TOPIC WHICH WILL BE USED BY THE NAVIGATION STACK TO FIND A PATH
    
""" 
class OcGridModific():
    def __init__(self):
        rospy.init_node('OcGridModifc', anonymous = True) 
        self.map_msg_queue = Queue()
        self.new_slam_map = False 

        self.OccupancyGrid = OccupancyGrid()

        # Write the occupancy grid message 
        self.OccupancyGrid.header = Header()
        self.OccupancyGrid.info = MapMetaData()
        self.OccupancyGrid.data = []


        timer = rospy.Timer(rospy.Duration(1/PUBLISH_FREQUENCY), self.publish_filtered_map)
        self.map_publisher = rospy.Publisher('/filtered_map', OccupancyGrid, queue_size = 10) 
        self.map_subscriber = rospy.Subscriber('/slam_map', OccupancyGrid, self.OccupancyGrid_cb) 

    # Callback function. It is invoked when /slam_map topic receives a new message.
    def OccupancyGrid_cb(self, msg):
        self.map_msg_queue.put(msg)
        self.new_lidar_map = True
    

    """
    Callback function.  Is called every 1/PUBLISH_FREQUENCY sec. 
    If a new slam map is received, the map will be filtered before being published to the topic /filtered_map.
    """
    def publish_filtered_map(self, event):
        if self.new_lidar_map:
            last_message = self.map_msg_queue[-1]
            self.OccupancyGrid.header = last_message.header
            self.OccupancyGrid.info = last_message.info
        

            # Start the filtering process
            unfiltered_map_as_np_array = map_to_matrix(self.map_msg_queue[-1])
            
            # filtered_map_as_np_array = ...
            filtered_map_as_OcGrid = matrix_to_map(filtered_map_as_np_array) 
            self.OccupancyGrid.data = filtered_map_as_OcGrid
            self.map_publisher.publish(self.OccupancyGrid)


if __name__ == '__main__':
    map = OcGridModific()
    while True:
        if rospy.is_shutdown():
            break
