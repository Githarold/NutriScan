
#!/usr/bin/env python2

import rospy
from std_msgs.msg import Int32
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from smach import State, StateMachine
from commander.srv import KeyCommand, KeyCommandResponse  # Importing the KeyCommand service

# Define the service callback function
def handle_key_command(req):
    # Implement logic based on the key command received
    response = ""
    if req.command == 'a':
        # Logic for stopping the robot if it's driving
        response = "Stopping the robot."
    elif req.command.isdigit() and 0 <= int(req.command) <= 9:
        # Logic for driving the robot to the specified room number
        response = f"Driving to room {req.command}."
    elif req.command == '?':
        # Logic for reporting the robot's location
        response = "Reporting the robot's location."
    else:
        response = "Invalid command."

    return KeyCommandResponse(response)

# Existing commander node code
# ...

if __name__ == '__main__':
    rospy.init_node('commander')

    # Set up the service server
    service = rospy.Service('key_command_service', KeyCommand, handle_key_command)

    # Existing state machine logic
    # ...
    commander = StateMachine('success')
    with commander:
        # Add states that you defined.
        StateMachine.add('IDLE', Idle(), transitions={'success':'RECIEVED'})
        StateMachine.add('RECIEVED', Recieved(), transitions={'success':'DRIVE'})
        StateMachine.add('DRIVE', Drive(room_num), transitions={'success':'IDLE'})

    commander.execute()
