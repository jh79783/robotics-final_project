#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher

    def lds_callback(self, scan):
        turtle_vel = Twist()
        forward_l = self.avg_distance(scan.ranges[350:359])
        forward_r = self.avg_distance(scan.ranges[0:10])
        forward = self.avg_distance([forward_l, forward_r])
        if (forward < 0.3) and (forward > 0):
            turtle_vel.linear.x = 0.1
            turtle_vel.angular.z = -1.5
           
        else:
            turtle_vel.linear.x = 0.18
            turtle_vel.angular.z = 0
        self.publisher.publish(turtle_vel)

    def avg_distance(self, scan):
        count = 0
        distance = 0

        for i in scan:
            if i != 0:
                count += 1
                distance += i

        if count != 0:
            avg_dis = distance/count
        else:
            avg_dis = 3

        if avg_dis != 0:
            self.temp = avg_dis
        if avg_dis == 0 :
            avg_dis = self.temp
        return avg_dis

def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()

if __name__ == "__main__":
    main()
