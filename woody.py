#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
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
Sonic = Sonar(brain.three_wire_port.a)
front_sensor = Distance(Ports.PORT14)
Armm_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
Armm_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
Armm = MotorGroup(Armm_motor_a, Armm_motor_b)
optical_3 = Optical(Ports.PORT3)


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
myVariable = 0
FOUNDBOT = Event()
message1 = Event()
NOBOT = Event()
ready_to_flip = Event()
drivetrain.set_turn_velocity(30,PERCENT)
drivetrain.set_drive_velocity(100,PERCENT)
dis_timer = 2
brain.screen.set_font(FontType.PROP40)



Armm.set_max_torque(100,PERCENT)
def Arm_Spin():
    Armm.spin(FORWARD)

def Arm_Stop():
    Armm.stop()
    
def Down_Spin():
    Armm.spin(REVERSE)

def Down_Stop():
    Armm.stop()

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

def seek_bot():
    global myVariable, FOUNDBOT, message1, NOBOT, ready_to_flip
    while not front_sensor.is_object_detected():
        drivetrain.turn(RIGHT)
        wait(0.01, SECONDS)
        wait(5, MSEC)
    while not front_sensor.object_distance(MM) < 300:
        drivetrain.drive(FORWARD)
        wait(0.01, SECONDS)
        wait(5, MSEC)
    wait(0.5,SECONDS)
    ready_to_flip.broadcast()

def when_started1():
    global myVariable, FOUNDBOT, message1, NOBOT, ready_to_flip
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(20, PERCENT)
    while not controller_1.buttonUp.pressing():
        wait(5, MSEC)
    seek_bot()

def onevent_controller_1buttonDown_pressed_0():
    global myVariable, FOUNDBOT, message1, NOBOT, ready_to_flip
    brain.program_stop()

def onevent_ready_to_flip_0():
    global myVariable, FOUNDBOT, message1, NOBOT, ready_to_flip
    drivetrain.set_drive_velocity(50,PERCENT)
    if optical_3.hue() >150:
            drivetrain.turn_for(RIGHT,180,DEGREES)
            drivetrain.drive_for(FORWARD,100,MM)
    else:
        for repeat_count in range(5):
            Armm.spin_for(FORWARD, 270, DEGREES)
            wait(0.01, SECONDS)
            Armm.spin_for(REVERSE, 270, DEGREES)
            wait(5, MSEC)
def onevent_ready_to_flip_1():
    drivetrain.set_drive_velocity(50,PERCENT)
    drivetrain.drive(FORWARD)


def kill_smth():
    global myVariable, FOUNDBOT, message1, NOBOT, ready_to_flip

controller_1.buttonR1.pressed(Arm_Spin)
Back_Bumper.pressed(freeze_bot)
Front_Bumper.pressed(freeze_bot)
controller_1.buttonR1.released(Arm_Stop)
controller_1.buttonR2.pressed(Down_Spin)
controller_1.buttonR2.released(Down_Stop)
controller_1.buttonB.pressed(Fsensor)
controller_1.buttonDown.pressed(onevent_controller_1buttonDown_pressed_0)
ready_to_flip(onevent_ready_to_flip_0)
ready_to_flip(onevent_ready_to_flip_1)
controller_1.buttonRight.pressed(when_started1)
controller_1.buttonLeft.pressed(kill_smth)

