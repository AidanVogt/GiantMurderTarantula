#!/bin/bash

# stop, reload, restart
sudo systemctl stop start_hexapod.service
sudo systemctl daemon-reload
sudo systemctl restart start_hexapod.service