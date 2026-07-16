# generate_eeprom.py

# 1 KB (1024 bytes) page size for STM32F051/F031
EEPROM_SIZE = 1024 

# Initialize the entire 1 KB page to 0xFF (standard blank flash state)
eeprom_data = bytearray([0xFF] * EEPROM_SIZE)

# Initialize the exact 192-byte C-Struct structure
struct_bytes = bytearray([0x00] * 192)

# --- Mapping to your actual EEprom_t Struct ---
struct_bytes[0]   = 0x01  # reserved_0 (ESC boot byte, MUST BE 1 to boot!)
struct_bytes[1]   = 0x02  # eeprom_version (Set to 2 to bypass older fallbacks)
struct_bytes[2]   = 0x01  # reserved_1 (Bootloader version)
struct_bytes[3]   = 0x01  # version.major
struct_bytes[4]   = 0x63  # version.minor (99)

struct_bytes[5]   = 160   # max_ramp (Default 160)
struct_bytes[6]   = 15    # minimum_duty_cycle (1.5% - solid starting torque)
struct_bytes[7]   = 1     # disable_stick_calibration (1 = Disabled to prevent drift)
struct_bytes[8]   = 0     # absolute_voltage_cutoff (0 = DISABLED! No more 49.5V bug)

struct_bytes[9]   = 100   # current_P
struct_bytes[10]  = 0     # current_I
struct_bytes[11]  = 100   # current_D
struct_bytes[12]  = 0     # active_brake_power

# 13 - 16: reserved_eeprom_3[4] (all 0)

struct_bytes[17]  = 0     # dir_reversed (0 = Normal)
struct_bytes[18]  = 0     # bi_direction (0 = Off)
struct_bytes[19]  = 0     # use_sine_start (0 = Off)
struct_bytes[20]  = 1     # comp_pwm (1 = On, complementary PWM is mandatory for active braking)
struct_bytes[21]  = 1     # variable_pwm (1 = On)
struct_bytes[22]  = 1     # stuck_rotor_protection (1 = On)
struct_bytes[23]  = 26    # advance_level (26 maps to 16 degrees timing in the newer format)
struct_bytes[24]  = 24    # pwm_frequency (24kHz)
struct_bytes[25]  = 100   # startup_power (100%)
struct_bytes[26]  = 55    # motor_kv (2200kv)
struct_bytes[27]  = 14    # motor_poles (14 poles)
struct_bytes[28]  = 1     # brake_on_stop (1 = On)
struct_bytes[29]  = 1     # stall_protection (1 = On)
struct_bytes[30]  = 5     # beep_volume (Comfortable mid-volume)
struct_bytes[31]  = 0     # telemetry_on_interval

# servo struct (Bytes 32-35)
struct_bytes[32]  = 125   # servo.low_threshold (125 * 2 + 750 = 1000us)
struct_bytes[33]  = 125   # servo.high_threshold (125 * 2 + 1750 = 2000us)
struct_bytes[34]  = 128   # servo.neutral (128 + 1374 = 1502us)
struct_bytes[35]  = 50    # servo.dead_band

struct_bytes[36]  = 0     # low_voltage_cut_off (0 = DISABLED for safety on bench)
struct_bytes[37]  = 50    # low_cell_volt_cutoff
struct_bytes[38]  = 0     # rc_car_reverse
struct_bytes[39]  = 0     # use_hall_sensors
struct_bytes[40]  = 5     # sine_mode_changeover_throttle_level
struct_bytes[41]  = 10    # drag_brake_strength
struct_bytes[42]  = 10    # driving_brake_strength

# limits struct (Bytes 43-44)
struct_bytes[43]  = 255   # limits.temperature (255 = Disabled for safety while testing)
struct_bytes[44]  = 0     # limits.current (0 = Disabled)

struct_bytes[45]  = 5     # sine_mode_power
struct_bytes[46]  = 2     # input_type (2 = SERVO_IN / Standard PWM explicitly forced)
struct_bytes[47]  = 0     # auto_advance

# Bytes 48 to 175: tune[128] (remains all 0x00)

# can struct (Bytes 176 to 191)
struct_bytes[180] = 1     # can.require_zero_throttle (1 = Safety arming required)

# Inject the 192-byte struct at the beginning of the EEPROM page
eeprom_data[0:192] = struct_bytes

# Write to output file
with open("eeprom.bin", "wb") as f:
    f.write(eeprom_data)

print("SUCCESS: 192-byte eeprom.bin generated to match eeprom.h exactly!")