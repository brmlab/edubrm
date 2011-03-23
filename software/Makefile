all: edubrm mainUi.py resources.py

mainUi.py: main.ui
	pyuic4 main.ui -o mainUi.py

resources.py:
	pyrcc4 resources.qrc -o resources_rc.py

clean:
	rm -f *.pyc modules/*.pyc mainUi.py resources_rc.py
