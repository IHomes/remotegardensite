filename=$(date -u +"%Y%m%d_%H%M%S")_%04d.jpg
/opt/vc/bin/raspistill -o /root/garden_monitor/images/$filename -tl 3600000 -t 36000000 > /root/garden_monitor/camera_log/camera.log 2>&1 &
