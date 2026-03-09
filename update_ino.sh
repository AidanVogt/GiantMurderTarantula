PORT=/dev/ttyACM0
CODE=/testing/arduino_xbox/

echo "Compiling and uploading to ${PORT}..."
arduino-cli compile --fqbn arduino:avr:uno ${CODE} --upload -p ${PORT} && echo "Done!"
