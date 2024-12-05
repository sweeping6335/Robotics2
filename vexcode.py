#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
motor_5 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
motor_9 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)


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
controller_1_left_shoulder_control_motors_stopped = True
controller_1_right_shoulder_control_motors_stopped = True

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global controller_1_left_shoulder_control_motors_stopped, controller_1_right_shoulder_control_motors_stopped, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            # check the buttonL1/buttonL2 status
            # to control motor_9
            if controller_1.buttonL1.pressing():
                motor_9.spin(FORWARD)
                controller_1_left_shoulder_control_motors_stopped = False
            elif controller_1.buttonL2.pressing():
                motor_9.spin(REVERSE)
                controller_1_left_shoulder_control_motors_stopped = False
            elif not controller_1_left_shoulder_control_motors_stopped:
                motor_9.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_left_shoulder_control_motors_stopped = True
            # check the buttonR1/buttonR2 status
            # to control motor_5
            if controller_1.buttonR1.pressing():
                motor_5.spin(FORWARD)
                controller_1_right_shoulder_control_motors_stopped = False
            elif controller_1.buttonR2.pressing():
                motor_5.spin(REVERSE)
                controller_1_right_shoulder_control_motors_stopped = False
            elif not controller_1_right_shoulder_control_motors_stopped:
                motor_5.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_right_shoulder_control_motors_stopped = True
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration

myVariable = 0
j = False
dis_timer = 3

def when_started1():
    global myVariable, j
    drivetrain.set_drive_velocity(100, PERCENT)
    while True:
    brain.screen.set_fill_color(Color.CYAN)
    brain.screen.draw_rectangle(0,0,479,239)
    while Back_Bumper.pressing() or Front_Bumper.pressing():
        remote_control_code_enabled = False
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(0,0,479,239)
        drivetrain.stop()
        brain.screen.set_font(FontType.PROP60)
        brain.screen.set_cursor(2.5,8.5)
        brain.screen.print(dis_timer)
        motor_5.spin(FORWARD)
        wait(1,SECONDS)
        motor_5.stop()
        wait(dis_timer - 1,SECONDS)
        brain.screen.clear_screen()
        remote_control_code_enabled = True
        brain.screen.set_fill_color(Color.CYAN)
        brain.screen.draw_rectangle(0,0,479,239)
        dis_timer = dis_timer * 2

def onevent_controller_1buttonA_pressed_0():
    global myVariable, j
    motor_9.spin_for(FORWARD, 90, DEGREES)
    motor_5.spin_for(FORWARD, 90, DEGREES)

# system event handlers
controller_1.buttonA.pressed(onevent_controller_1buttonA_pressed_0)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started1()
