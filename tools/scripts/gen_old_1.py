# https://wiki.am32.ca/development/Open-ESC-EEPROM-Format.html

# generate_eeprom.py

# 1 KB (1024 bytes) page size for STM32F051/F031
EEPROM_SIZE = 1024 

# Initialize the entire 1 KB page to 0xFF (standard blank flash state)
eeprom_data = bytearray([0xFF] * EEPROM_SIZE)

# Define the exact 48-byte AM32 configuration structure
config_bytes = bytearray([
    # === COMMON SECTION (First 18 Bytes) ===
    0x01,        # [0]  ESC boot byte (Must be 1 to boot main app!)
    0x00,        # [1]  EEPROM version 
    0x01,        # [2]  Bootloader version
    0x01,        # [3]  Firmware version major
    0x04,        # [4]  Firmware version minor
    # [5-16] ESC name: "RVS V2      " (12 bytes)
    0x52, 0x56, 0x53, 0x20, 0x56, 0x32, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
    0x00,        # [17] Direction reversed default (0 = Normal)

    # === HARDWARE SPECIFIC (30 Bytes total, including Version 1 additions) ===
    0x00,        # [18] Bidirectional mode (0 = Off)
    0x00,        # [19] Sinusoidal startup (0 = Off)
    0x01,        # [20] Complementary PWM (1 = On)
    0x01,        # [21] Variable PWM frequency (1 = On)
    0x01,        # [22] Stuck rotor protection (1 = On)
    0x02,        # [23] Timing advance x7.5 (2 = 15 degrees)
    0x18,        # [24] PWM frequency (0x18 = 24kHz)
    0x64,        # [25] Startup power (0x64 = 100%)
    0x37,        # [26] Motor KV in increments of 40 (0x37 = 55 -> 2200kv)
    0x0e,        # [27] Motor poles (0x0e = 14 poles)
    0x01,        # [28] Brake on stop (1 = On)
    0x00,        # [29] Stall protection (0 = Off)

    # === Version 1 Additions (Firmware 1.65+) ===
    0x08,        # [30] Beep volume (range 0 to 11)
    0x00,        # [31] 30ms telemetry output (0 = Off)
    0x80,        # [32] Servo low value =  (value*2) + 750us
    0x80,        # [33] Servo high value = (value *2) + 1750us
    0x80,        # [34] Servo neutral base 1374 + value microseconds. i.e. 128 = 1502 us, default 128 (0x80)
    0x32,        # [35] Servo dead band. 0-100, applied to either side of neutral default 50 (0x32)
    0x00,        # [36] Low voltage cut-off (0 = Off)
    0x32,        # [37] Low voltage threshold (0x32 = 50 -> 3.0v)
    0x00,        # [38] RC car type reversing (0 = Off)
    0x00,        # [39] Use Hall sensors if equipped (0 = Off)
    0x08,        # [40] Sine Mode Range 5-25% (0x08 = 8%)
    0x0a,        # [41] Drag Brake Strength (0x0a = 10, full strength)

    # === Reserved / Padding Bytes (To fill out the 48-byte structure) ===
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00  # [42-47] Reserved
])

# Inject the 48-byte configuration structure at the absolute start of our 1 KB page
eeprom_data[0:48] = config_bytes

# Save output binary file
with open("eeprom.bin", "wb") as f:
  f.write(eeprom_data)

print("SUCCESS: eeprom.bin generated matching your exact hardware specs!")