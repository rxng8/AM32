#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [[ "${1:-}" == "--bootloader-only" ]]; then
	openocd -f flash_bootloader_only.cfg
else
	rm -f fw.bin
	# cp ../../obj/AM32_SISKIN_11A_F051_2.20.bin fw.bin
	cp ../../obj/AM32_RVS_V2_F051_2.20.bin fw.bin
	python gen.py
	openocd -f flash_firmware.cfg
fi
