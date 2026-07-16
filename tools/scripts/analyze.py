# %%

eeprom_data = bytearray([0xFF] * 1024)  # Create a 1KB EEPROM page filled with zeros
tmp = [int(b) for b in eeprom_data]  # Convert bytearray to list of integers
len(tmp)


# %%


# Write to output file
with open("tmp.bin", "rb") as f:
  eeprom_data_read = bytearray(f.read())

eeprom_data[:len(eeprom_data_read)] = eeprom_data_read  # Update the EEPROM data with the read data


# %%


# eeprom_data = [int.from_bytes(eeprom_data[i:i+2], 'little') for i in range(0, len(eeprom_data), 2)]
# eeprom_data = [x for x in eeprom_data if x != 0xFFFF]  # Filter out 0xFFFF values
# eeprom_data

eeprom_data_read = [int(b) for b in eeprom_data_read]  # Convert bytearray to list of integers

# %%

len(eeprom_data_read)

# %%

eeprom_data_read  # Display the first 10 bytes of the EEPROM data
