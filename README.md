## Welcome to this world

### [Trick] to remove unneccessary .pyc files

	find . -name "*.pyc" | xargs rm

### Run the project

Before run the project, you should install bower, pip >= 1.4.1 and python 2.7

	bower install
	pip install -r requirements.txt
	python application.py
	python chat.py

### To Test Application

This application use nose as testrunner, you must install nose before run the test

	python test.py

Note: If you are using Mac OS X, you must install libjpeg

	pip uninstall PIL
	brew install libjpeg
	pip install PIL

Note: If you are using ubuntu, you can install pillow by:

    sudo apt-get install libjpeg-dev
    pip install -I pillow
