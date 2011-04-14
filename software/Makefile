all: edubrm mainUi.py resources_rc.py modules/ModuleDebugUi.py

mainUi.py: main.ui
	pyuic4 $< -o $@

resources_rc.py: resources.qrc
	pyrcc4 $< -o $@

modules/ModuleDebugUi.py: modules/ModuleDebug.ui
	pyuic4 $< -o $@

clean:
	rm -f *.pyc *Ui.py modules/*.pyc modules/*Ui.py resources_rc.py
