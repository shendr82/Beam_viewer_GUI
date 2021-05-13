# Beam_viewer_GUI

Running TDMS_connect_with_GUI3.py file should start the "Beam viewer GUI" app.

Files needed to run app:
	TDMS_class_for_GUI2.py
	TDMS_class_multi_files2.py
	Beam_GUI8.py
	TDMS_connect_with_GUI3.py

TDMS files:
	- copy TDMS files on your drive
	- some files are in this pakage (see TDMS files directory)

CMOS files:
	- copy CMOS (bmp images) on your drive
	- directory name should be shotID
	- files not included in this pakage (see on Beam: /data/W7-X/APDCAM/'shotID')

IMPORTANT:
	Insall and use nptdms 0.18.1 version (conda install -c conda-forge nptdms=0.18.1)

	TDMS_class_for_GUI2.py
		Line 167 - Check TDMS file location on you drive
    		Line 766 - Check CMOS file location on you drive (directory should be shotID)	