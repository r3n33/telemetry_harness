#!/usr/bin/env python
# Software License Agreement (BSD License)
#
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
import math

def publisher():
    JointPositions = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    sub = rospy.Subscriber('/joint_states', JointState, callback_calling, JointPositions )
    pub = [ rospy.Publisher('/hros5/RShoulderPitch_position_controller/command', Float64, queue_size=2) , rospy.Publisher('/hros5/LShoulderPitch_position_controller/command', Float64, queue_size=2) , rospy.Publisher('/hros5/RShoulderRoll_position_controller/command', Float64, queue_size=2)  , rospy.Publisher('/hros5/LShoulderRoll_position_controller/command', Float64, queue_size=2) , rospy.Publisher('/hros5/RElbowPitch_position_controller/command', Float64, queue_size=2), rospy.Publisher('/hros5/LElbowPitch_position_controller/command', Float64, queue_size=2) ]
    rospy.init_node('telemetry_publisher', anonymous=True)
    rate = rospy.Rate(50) # 10hz
    position = 0.0
    while not rospy.is_shutdown():
	#One at a time for testin
	pub[0].publish(JointPositions[0])
        pub[1].publish(JointPositions[1])
	pub[2].publish(JointPositions[2])
	pub[3].publish(JointPositions[3])
	pub[5].publish(JointPositions[5])
	pub[4].publish(JointPositions[4])
	
	#for index, publisher in enumerate(pub):
	#	publisher.publish( JointPositions[index] )
        rate.sleep()

def callback_calling(data, JointPositions):
    #print data
    for ( index, name) in enumerate(data.name):
        if name == 'joint_1':
	    #Right shoulder pitch.. invert positions
	    JointPositions[0] = data.position[ index ] + math.pi
	    if JointPositions[0] > math.pi:
		JointPositions[0] -= 2 * math.pi
        if name == 'joint_2':
	    # Left sholder pitch.. invert position
            JointPositions[1] = data.position[ index ] + math.pi
	    if JointPositions[1] > math.pi:
	        JointPositions[1] -= 2 * math.pi
        if name == 'joint_3':
	    #Right shoulder roll..
            JointPositions[2] = -data.position[ index ] + math.pi
	    if JointPositions[2] > math.pi:
		JointPositions[2] -= 2 * math.pi
	    print JointPositions[2]
        if name == 'joint_4':
	    #Left sholder roll.. invert direction and position
            JointPositions[3] = -data.position[ index ] + math.pi
	    if JointPositions[3] > math.pi:
		JointPositions[3] -= 2 * math.pi
        if name == 'joint_5':
            JointPositions[4] = data.position[ index ]
        if name == 'joint_6':
	    #Left elbow pitch.. no change
            JointPositions[5] = data.position[ index ]# + math.pi
	    #if JointPositions[5] > math.pi:
		#JointPositions[5] -= math.pi
            #position = data.position[ index ]
	    #print 'donkey butt'
	    #print position
	    #JointPositions[0] = position

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
