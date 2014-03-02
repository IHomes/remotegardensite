filename=$(date -u +"%Y%m%d_%H%M%S")_%04d.jpg
/opt/vc/bin/raspistill -o /root/garden_monitor/images/$filename -tl 30000 -t 90000 > /root/garden_monitor/camera_log/camera.log 2>&1 &
