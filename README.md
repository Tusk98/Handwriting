# Handwriting

I previous had text_segmentation working where if I ran 

```
python3 transform.py -i test.jpg
``` 

I would be able to "scan" the image into what you see in result.jpg 

I then started working on model for recognizing handwritten digits, but I'm having compatibility problems with python's numpy and tensorflow and opencv, I'm gonna see if there's a way that I can fix it.  

If you want to try transform.py the dependencies are below: 

## Dependencies (Model + GUI) Only on Windows so far
 - Python 3.X 
	-[numpy](https://pypi.org/project/numpy/)
	-[keras](https://pypi.org/project/Keras/)
	-[tensorflow](https://pypi.org/project/tensorflow/)
	
	Below are the requirements if you want to use the gui
	-[Pillow(PIL)](https://pypi.org/project/Pillow/)
	-[win32gui] For this one you need to use ```pip install pywin32```

## Dependencies (Scanner) 
 - Python 3.X
	- [numpy](https://pypi.org/project/numpy/)
	- [OpenCV](https://pypi.org/project/opencv-python/)
	- [scikit-image](https://pypi.org/project/scikit-image/)
