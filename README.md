# python-opencv-object-moving
build from  
https://blog.gtwang.org/programming/opencv-motion-detection-and-tracking-tutorial/  
https://docs.opencv.org/4.1.2/dd/d43/tutorial_py_video_display.html

Python     3.7.5, 
python-vlc, 
libopencv  4.1.2, 
opencv     4.1.2, 
py-opencv  4.1.2 conda-forge  

pip install numpy  
pip install matplotlib  
pip install opencv-python  
pip install python-vlc  

Start recording when an object is detected  
Stop recording when no object is detected in 5 minutes  
For each videos no longer than 30 minutes  
Keep videos less than 21 days  

Please modify the parameters carefully  
When changing "vdoRoot" in python_opencv_objectmoving.py and  
"timedelta (day = 21)" in scanDir.py  

Run  
python python_opencv_objectmoving.py  
