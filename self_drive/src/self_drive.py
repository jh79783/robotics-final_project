#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher

    def lds_callback(self, scan):
        forward_l = self.avg_distance(scan.ranges[350:359])
        forward_r = self.avg_distance(scan.ranges[0:10])
        forward = self.avg_distance([forward_l, forward_r])
        front_side = self.avg_distance(scan.ranges[30:50])
        if (forward < 0.3) and (forward > 0):
            self.go_turn(0.1, -1.5)
           
        else:
            if (front_side < 0.25) and (front_side > 0):
                self.go_turn(0.18, -0.5)
            elif front_side >= 0.25:
                self.go_turn(0.15, 0.5)
            else:
                self.go_turn(0.18, 0)
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

    def go_turn(self, x, z):
            turtle_vel = Twist()
            turtle_vel.linear.x = x
            turtle_vel.angular.z = z
            self.publisher.publish(turtle_vel)

def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()

if __name__ == "__main__":
    main()
