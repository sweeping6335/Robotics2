#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
Arm_1 = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
Arm_2 = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)
Back_Bumper = Bumper(brain.three_wire_port.h)
Front_Bumper = Bumper(brain.three_wire_port.g)
left_motor_a = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
front_sensor1 = Distance(Ports.PORT13)
Sonic = Sonar(brain.three_wire_port.a)
front_sensor = Distance(Ports.PORT14)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            drivetrain_left_side_speed = controller_1.axis3.position() + controller_1.axis1.position()
            drivetrain_right_side_speed = controller_1.axis3.position() - controller_1.axis1.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code
drivetrain.set_turn_velocity(100,PERCENT)
drivetrain.set_drive_velocity(100,PERCENT)
dis_timer = 2
brain.screen.set_font(FontType.PROP40)



Arm_1.set_max_torque(100,PERCENT)
Arm_2.set_max_torque(100,PERCENT)
Arm_2.set_velocity(100,PERCENT)
Arm_1.set_velocity(100,PERCENT)
def Arm_Spin():
    Arm_1.spin(FORWARD)
    Arm_2.spin(FORWARD)

def Arm_Stop():
    Arm_1.stop()
    Arm_2.stop()
    
def Down_Spin():
    Arm_1.spin(REVERSE)
    Arm_2.spin(REVERSE)

def Down_Stop():
    Arm_1.stop()
    Arm_2.stop()

def freeze_bot():
    global myVariable, dis_timer
    remote_control_code_enabled = False
    brain.screen.set_fill_color(Color.RED)
    brain.screen.draw_rectangle(0,0,479,239)
    drivetrain.stop()
    brain.screen.set_font(FontType.PROP60)
    brain.screen.set_cursor(2.5,8.5)
    brain.screen.print(dis_timer)
    wait(dis_timer,SECONDS)
    brain.screen.clear_screen()
    remote_control_code_enabled = True
    brain.screen.set_fill_color(Color.CYAN)
    brain.screen.draw_rectangle(0,0,479,239)
    dis_timer = dis_timer * 2

def Fsensor():
    brain.screen.set_font(FontType.PROP30)
    while brain.battery.capacity():
        brain.screen.set_cursor(1,1)
        brain.screen.print(front_sensor.object_distance(MM))
        wait(0.1,SECONDS)
        brain.screen.clear_row(1)
        brain.screen.set_cursor(2,1)
        brain.screen.print(front_sensor.object_size())
        brain.screen.set_cursor(3,1)
        brain.screen.print(front_sensor.object_velocity())
        brain.screen.set_cursor(4,1)
        brain.screen.print(Sonic.distance(MM))
        
    


controller_1.buttonR1.pressed(Arm_Spin)
Back_Bumper.pressed(freeze_bot)
Front_Bumper.pressed(freeze_bot)
controller_1.buttonR1.released(Arm_Stop)
controller_1.buttonR2.pressed(Down_Spin)
controller_1.buttonR2.released(Down_Stop)
controller_1.buttonB.pressed(Fsensor)
