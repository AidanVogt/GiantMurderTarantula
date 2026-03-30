PORT=/dev/ttyACM0
CODE=./testing/i2c_demo

echo "Compiling and uploading to ${PORT}..."
arduino-cli compile --fqbn arduino:avr:uno ${CODE} --upload -p ${PORT} && echo "Done!"
