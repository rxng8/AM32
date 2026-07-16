# generate_eeprom.py

EEPROM_SIZE = 1024
eeprom_data = bytearray([0xFF] * EEPROM_SIZE)

# Initialize the exact 192-byte C-Struct structure
struct_bytes = bytearray([0xFF] * 192)

# --- Base Header (Indices 0 - 4) ---
struct_bytes[0]   = 0x01  # reserved_0 (ESC boot byte). Default to 0x01 = 1
struct_bytes[1]   = 0x03  # eeprom_version. Default to 0x03 = 3
struct_bytes[2]   = 0x12  # reserved_1. Default to 0x12 = 18
struct_bytes[3]   = 0x02  # version.major. Default to 0x02 =2
struct_bytes[4]   = 0x14  # version.minor. Default to 0x14 = 20

# --- Basic Settings (Indices 5 - 12) ---
struct_bytes[5]   = 0xA0   # max_ramp (0.1% per ms to 25% per ms). Default to 0xA0 = 160 (16% per ms)
struct_bytes[6]   = 0x04     # minimum_duty_cycle (0.2% to 51%). Default to 0x04 = 4 (2%)
struct_bytes[7]   = 0x00     # disable_stick_calibration. Default to 0
struct_bytes[8]   = 0x0A    # absolute_voltage_cutoff (in 0.5v increments). Default to 0x0A = 10
struct_bytes[9]   = 0x64   # current_P (0-255). Default to 0x64 = 100
struct_bytes[10]  = 0x00     # current_I (0-255). Default to 0x00 = 0
struct_bytes[11]  = 0x32   # current_D (0-255). Default to 0x32 = 50
struct_bytes[12]  = 0x02     # active_brake_power (1-5 percent). Default to 0x02 = 2

# --- CRSF / Reserved Inputs (Indices 13 - 16) ---
struct_bytes[13]  = 0xFF     # reserved_eeprom_3[0]. Default to 0xFF
struct_bytes[14]  = 0xFF     # reserved_eeprom_3[1]. Default to 0xFF
struct_bytes[15]  = 0xFF     # reserved_eeprom_3[2]. Default to 0xFF
struct_bytes[16]  = 0xFF     # reserved_eeprom_3[3]. Default to 0xFF

# --- Core Motor Configuration (Indices 17 - 31) ---
struct_bytes[17]  = 0x00     # dir_reversed. Default to 0x00 = 0
struct_bytes[18]  = 0x00     # bi_direction. Default to 0x00 = 0
struct_bytes[19]  = 0x00     # use_sine_start. Default to 0x00 = 0
struct_bytes[20]  = 0x01     # comp_pwm. Default to 0x01 = 1
struct_bytes[21]  = 0x01     # variable_pwm. Default to 0x01 = 1
struct_bytes[22]  = 0x01     # stuck_rotor_protection. Default to 0x01 = 1
struct_bytes[23]  = 0x1A    # advance_level (Set to 26 so temp_advance = 16 after subtracting 10). Default to 0x1A = 26
struct_bytes[24]  = 0x18    # pwm_frequency. Default to 0x18 = 24
struct_bytes[25]  = 0x64    # startup_power. Default to 0x64 = 100
struct_bytes[26]  = 0x37   # motor_kv. Default to 0x37 = 55 => 2220kv
struct_bytes[27]  = 0x0E    # motor_poles. Default to 0x0E = 14
struct_bytes[28]  = 0x00     # brake_on_stop. Default to 0
struct_bytes[29]  = 0x00     # stall_protection. Default to 0
struct_bytes[30]  = 0x05    # beep_volume. Default to 0x05 = 5
struct_bytes[31]  = 0x00     # telemetry_on_interval. Default to 0x00 = 0

# --- Servo Configuration (Indices 32 - 35) ---
struct_bytes[32]  = 0x80   # servo.low_threshold. Default to 0x80 = 128 => 1006
struct_bytes[33]  = 0x80   # servo.high_threshold. Default to 0x80 = 128 => 2006
struct_bytes[34]  = 0x80   # servo.neutral. Default to 0x80 = 128 => 1502
struct_bytes[35]  = 0x32     # servo.dead_band. Default to 0x32 = 50

# --- Additional Protections & Logic (Indices 36 - 42) ---
struct_bytes[36]  = 0x00     # low_voltage_cut_off. Default to 0x00 = 0
struct_bytes[37]  = 0x32     # low_cell_volt_cutoff. Default to 0x32 = 50 (2.5V per cell)
struct_bytes[38]  = 0x00     # rc_car_reverse. Default to 0x00 = 0
struct_bytes[39]  = 0x00     # use_hall_sensors. Default to 0x00 = 0
struct_bytes[40]  = 0x0F    # sine_mode_changeover_thottle_level. Default to 0x0F = 15
struct_bytes[41]  = 0x0A     # drag_brake_strength. Default to 0x0A = 10
struct_bytes[42]  = 0x0A     # driving_brake_strength. Default to 0x0A = 10

# --- Limits & Hardware Overrides (Indices 43 - 47) ---
struct_bytes[43]  = 0x8D   # limits.temperature. Default to 0x8D = 141 (disable)
struct_bytes[44]  = 0x66    # limits.current. Default to 0x66 = 102 (disable)
struct_bytes[45]  = 0x06    # sine_mode_power. Default to 0x06 = 6
struct_bytes[46]  = 0x00     # input_type. Default to 0x00 = 0 (auto)
struct_bytes[47]  = 0x00     # auto_advance. Default to 0x00 = 0

# --- Custom Audio/Tune Array (Indices 48 - 175) ---
# Fills 128 elements with a default value (e.g., 0)
struct_bytes[48:176] = [0xFF] * 128  # tune[128]

# --- CAN Bus Configuration Block (Indices 176 - 191) ---
struct_bytes[176] = 0xFF     # can.can_node
struct_bytes[177] = 0xFF     # can.esc_index
struct_bytes[178] = 0xFF     # can.require_arming
struct_bytes[179] = 0xFF    # can.telem_rate
struct_bytes[180] = 0xFF     # can.require_zero_throttle
struct_bytes[181] = 0xFF    # can.filter_hz
struct_bytes[182] = 0xFF     # can.debug_rate
struct_bytes[183] = 0xFF     # can.term_enable
struct_bytes[184:192] = [0xFF] * 8  # can.reserved[8]

# --- Copy Struct into the Flash Page ---
eeprom_data[0:192] = struct_bytes

# Save as binary file
with open("eeprom.bin", "wb") as f:
    f.write(eeprom_data)