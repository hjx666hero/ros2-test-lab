@echo off
title ROS 2 Humble - robotics test lab
wsl -d ROS2-Humble --cd /mnt/f/ros_workspace
if errorlevel 1 pause
