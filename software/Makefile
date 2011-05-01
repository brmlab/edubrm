all: edubrm mainUi.py resources_rc.py modules/ModuleAUi.py modules/ModuleBUi.py modules/ModuleCUi.py modules/ModuleDebugUi.py

mainUi.py: main.ui
	pyuic4 $< -o $@

resources_rc.py: resources.qrc
	pyrcc4 $< -o $@

modules/Module%Ui.py: modules/Module%.ui
	pyuic4 $< -o $@

clean:
	rm -f *.pyc *Ui.py modules/*.pyc modules/*Ui.py resources_rc.py
