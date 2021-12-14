# Mapping Multimodal Physiological Sensors to Control a Robot Agent

This repository contains python scripts to connect sensor data from an Emotiv® Insight® EEG and an Empatica® E4® wristband, process the data, and map it to controls for a LEGO® MINDSTORMS® EV3 robot.

The architecture runs multiple scripts at once, and sends the data using MQTT. Each individual sensor uses a script to retrieve the data from the sensor, then sends that data (or a transformed version of it) to an intermediatary script which processes the multimodal sensor data and sends movement commands to the EV3 robot via MQTT. 
