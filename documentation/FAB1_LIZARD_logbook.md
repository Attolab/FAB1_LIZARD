---
18/03/22

Call Seb
---

Pour le changement de consigne du LIZARD avec un programme labview (server) il recommande d'utiliser la dernière version de pymodaq avec le module pid.
Dans ce cas en effet est déjà implémenté l'idée de "fake" actuator (daq_move qui permet de changer la consigne du pid).
Il faudrait ensuite que ce fake actuator soit un client tcp, il recevera alors les consignes du server.


TODO
---

* installer un nouvel environnement python sur le pc central de fab1 : FAB1_LIZARD_pmd_355
* installer la dernière version de pmd
* installer les plugins
* check communication avec le scope et le piezo
* check lizard avec cette version de pmd (3.5.5)
* en principe la suite devrait rouler…


Installation pmd
---

On a créé l’environnement FAB1_LIZARD_pmd355 sur le pc beamline.

On a suivi ces commandes pour l’installation de pmd (avant on a mis a jour conda) : cf ici : https://github.com/CEMES-CNRS/PyMoDAQ/issues/70

conda create -n FAB1_LIZARD_pmd355 python=3.8
conda activate FAB1_LIZARD pmd355
pip install pymodaq
pip install pyqt5

-> on lance un dashboard ça fonctionne !

Installation du plugin "Physical Measurements Hardware" (contient le plugin pour lire le lecroy waverunner) via le plugin_manager.

L’installation n’a pas bien marchée car si on lance un viewer le plugin lecroy n’apparaît pas dans la liste. Dans les logs on a :

2022-03-18 15:53:15,973 - pymodaq.viewer1D_plugins - WARNING - daq_1Dviewer_LecroyWaverunner plugin couldn't be loaded due to some missing packages or errors: DLL load failed while importing win32api: Le module spécifié est introuvable.

Creation projet Pycharm : On crée un projet pycharm associé.

Pour résoudre le problème on essaie ça : https://stackoverflow.com/questions/58612306/how-to-fix-importerror-dll-load-failed-while-importing-win32api

conda install pywin32

-> ça fonctionne !


TODO
---

* Inclure dans le plugin pmd la dépendance au paquet pywin32



---
17/03/22

The server computer is the one that is NOT actually connected to the device (actuator or detector).

What we want
---

The beamline computer will be the client. Here we have to kind of create a "fake" actuator that would control the setpoint of the LIZARD.

VMI computer (server). Here we will have a DAQ_Move TCP that will send orders to the beamline  computer.







---
17/03/22

Branchement piezo (piezosystem iena)
---

Sortie USB de la boîte Alice/Mariuz.

cf 10/07/20

"
Quand on fait un find home avec le piezo il arrive à 27.9 um... il semble que les mouvements sont relatifs à cettte position.

-> il faut vérifier que la commande manuelle du piezo soit à zero : bouton qui tourne à mettre à fond vers la gauche (counter-clockwisde). Dans ces conditions il semble réagir correctement. Le find home va bien à zero et les mouvements relatifs et absolus fonctionnent. Par contre même pour epsilon=5nm il semble qu'il valide des positions en dehors de cet intervalle ce qui est assez bizarre... On dirait que la précision maximale est de 10nm...
"

cf 02/03/21

"
Crazy piezo
-----------

Sometimes the reading of the piezo through pymodaq go crazy. It sounds like restarting the controller fix the problem.
"

-> si on suit ces deux trucs ça fonctionne


LOCKING!!
---

It locked for more than an hour.
We put the current packages (from C:\ProgramData\Anaconda3\Lib\site-packages):

pymodaq
pymodaq_̣pid_models
pymodaq_plugins

in a folder 220317_backup on the github repository. We do in this nasty way because we probably changed the code of the pymodaq 1.6.3 version.



---
15/03/22

Create FAB1_LIZARD repository.


Environnement python (créé le 19/01/21): pymodaq_lizard sur le pc central de FAB1.

un dépôt privé a été créé sur le github Attolab : pymodaq_LIZARD_FAB1. On ne va plus rien mettre dans ce dépôt (il devrait disparaître, pour être remplacé par FAB1_LIZARD). Il contient plusieurs PIDModel (last commit 08/03/21 sur PIDModelLIZARD.py).

TODO
---

* Enregistrer le fichier qui contient les versions de tous les paquets de l'environnement python pymodaq_lizard.

---
16/03/22

Environnement python sur pc central FAB1
---

Si on lance par exemple un daq_move dans l’environnement pymodaq_lizard ça plante.

En fait il semble qu’on soit resté dans l’environnement de base : le 21/01/21 :  "Pour le moment on travaille toujours dans l'environnement de base de Anaconda (C:\ProgramData\Anaconda3\...)"

-> oui le projet est bien  dans C:\ProgramData\Anaconda3\Lib\site-packages\pymodaq

On a pu ouvrir le projet récent correspondant.

Chelou : si on fait un conda env list il ne voit pas cet environnement. (Il ne voit que l’environnement de base C:\Users\attose1\Anaconda3 et non C:\ProgramData\Anaconda3\) Probablement un truc chelou avec l’installation d’anaconda… Il semble qu’il y ait 2 anaconda d’installés sur ce pc…








--------------------------------------

--------------------------------------

--- 08/03/21 ---

Save the axis of the oscilloscope
---------------------------------

The correspondance between the indices of the scope and the values in time should be saved in a 1D array called "X_axis", saved in the same directory as "Data". It is not 1D data strictly speaking but still is saved in a sub directory of Data1D since it corresponds to the oscilloscope data.

It should not be confused with the scan steps array !



--- 02/03/21 ---

Crazy piezo
-----------

Sometimes the reading of the piezo through pymodaq go crazy. It sounds like restarting the controller fix the problem.


TESTS
-----------

- It would be nice to be able to launch another stabilized scan or calibration scan at the end of the stabilized scan without closing the program.
	-> seems to work. Has to be tested with a real signal.

- Test the security while calling do_stabilized_scan for example without calibration_scan_done.

- Do the initialization of the h5 file in a dedicated function.

- There is something wrong if the user PAUSE the feedback loop and STOP it. After that it is not possible to restart the loop again.



--- 01/03/21 ---

Stabilized scan is saved !
-------------------------


-> we used the same structure for the do_stabilized_scan method than for the do_calibration method. i.e. connect signals with the oscilloscope and use wait_for_det_done method etc ……
-> and it seems like using self.channel_pytables_array (i.e. define it as a class attribute) is no longer a problem…



--- 26/02/21 ---

Calibration scan
----------------

- the parameters of the fitted ellipsis should be saved in the metedata.

Saving
------

- check that it is not necessary to define a new file name for the h5 file at launch of the program.


First stabilized scan ?
-----------------------

Scan2.h5 h 200nm, 20nm steps, 20 iterations per step


Test live change of Kp
----------------------
	-> this has been done (02/03/21) checking that the parameter value of the UI is the same as the value in PIDRunner.pid



Enregistrement foirreux…
------------------------

channel_pytables_array est bien initialisé mais on ne comprend pas pourquoi il est pas rempli au fur et à mesure du scan de stabilisation…


--- 25/02/21 ---

210224/scan7.h5 : Scan002 comes from the saving of the stabilized scan so it means that the initialization of saving was working at least partially.

Il a créé aussi un array Data dans CH000 qui fait 500 (samples of the scope: ok) * 1000 (50*20 which was the default number of setpoints * number of iterations per step at this time): so it sounds good ! This array is filled with zeros.

-> so it seems like __init_saving_stabilized_scan works properly.


New default parameters for the stabilized scan
----------------------------------------------

20 itérations semble un minimum pour que le système est le temps de se stabiliser sur une consigne avant de la changer.
Pas de 20nm raisonnable.
10 pas fait 200nm.

20*10=200 itérations

200*0.5 seconde = 100 secondes = 1.5 minute



LOG message from LIZARD
-----------------------

	self.pid_controller.log_signal.emit("text")



Bug do_stabilized_scan
----------------------

	il y a un problème au niveau de

		channel_pytables_array

	-> solved ! self.stabilized_scan_shape was not initialized

	Now the stabilized scan node is created. Ça semble bien fonctionner jusqu’à créer un pytables array de la bonne taille. Puis ça plante à la première itération.

	15h: il plante à la ligne 593: ça doit être parce qu’on construisait pas bien self.channel_pytables_array dans __init_saving_stabilized_scan



TO BE CHECKED
-------------

	check that the update for the pid parameters are done properly.
	it would be nice to print the values that are stored in the PIDRunner.pid object.



--- 24/02/21 ---

New definition of phase_time_zero
---------------------------------

The definition of phase_time_zero is now done at first call of convert_input.
It seems to work better like that.

Kp=0.4 Ki=0.05 Kd=0 epsilon=0.005

Typical setpoint change
-----------------------

A typical setpoint change is 0.6 rad.


--- 23/02/21 ---

Measure phase_time_zero
-----------------------

It seems like we have problems by measuring the phase at time zero after the calibration scan.
We will try by defining it at first call of convert_input (which is done when the user push the PLAY button).


Declaration of signals
----------------------

In DAQ_PID the signals are not declared in the constructor but before… ??

-> it seems normal to declare it like that : see notes on pyqt and https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html



--- 19/02/21 ---

Move done signal
----------------

	DAQ_Move.move_done_signal(str, float)

str: title of the module
float: position !

This signal is connected to LIZARD.move_done in do_calibration



Get the actuator object (DAQ_Move)
-----------------------

	self.pid_controller.actuator_modules[0]





--- 18/02/21 ---

The feedback loop seems to work with Kp = 0.4 and Ki = 0.05, epsilon = 0.01


--- 17/02/21 ---

LIZARDModel.curr_position is not updated correctly while the PID loop is running.
We can access it through the actuator module ?:

	DAQ_PID.actuator_modules[0].current_position

??





--- 12/02/21 ---

Workflow after calibration scan
-------------------------------

At the end of the calibration scan, the parameters of the ellipsis are set + the phase measured at time zero.

(*) click INIT PID: this will not produce any effect to the user except that the PLAY and PAUSE button are now available.




Colors for ROI
--------------

Use yellow and green colors for the modulated signals because you can see them even with the glasses.

FAB1 optimize SB
----------------

Use joystick MOTOR A and MOTOR B that move the axis of the mirror before drill mirror.

PID input
---------

PID input should be 

	PID input = Current point - Set point

?? It looks like it is not the case.


--- 05/02/21 ---

Au démarrage du scan stabilisé, on connecte le signal grab_done du scope avec la fonction self.det_done et c’est elle qui se charge d’enregistrer les données dans le fichier h5.
-> Non ça n’est pas très pratique parce qu’on aimerait bien enregistrer aussi la mesure de la phase, qui est donnée par la fonction convert_input.
-> C’est pour ça qu’on choisit d’effectuer l’enregistrement dans la fonction convert_input.


Initialize PyTables scope array in stabilized scan
--------------------------------------------------

To initialize this array, we can save in a variable the array that we used in the calibration scan.



--- 04/02/21 ---

Workflow after calibration (see 25/01/21)
--------------------------

(*) Click INIT PID
(*) Click the PLAY button
(*) Click (uncheck) the PAUSE button



--- 03/02/21 ---

PIDModelGeneric
---------------

-> This class is empty it sounds useless…

TEST: does the program run if we remove the inheritence relation with this class ??

PIDModelLIZARD.det_done
-----------------------

-> check when this function is called and if enter the if statement.


PIDModelLIZARD.convert_input
----------------------------

In this method we get the spectrum from the scope. It sounds to be the good place to save the data ??

TEST DE L’ENREGISTREMENT DES DONNÉES LORS DU SCAN DE CALIBRATION
----------------------------------------------------------------

Ça fonctionne ! :D

On a vérifié aussi la méthode PIDModelLIZARD.det_done : effectivement on rentre dans la méthode à chaque fois que des données arrivent, lors d’un scan de calibration. Par contre on ne rentre pas dans la condition if lors d’un scan de calibration.

On a commité/pushé cette version.

Scan naming
-----------

It could be nice to name a scan : Scan15h32 rather than Scan002 ??
-> does not sounds so important but the time of the creation of the node should be registered in the metadata.



Stabilized scan
---------------

As a stabilized scan is running (self.stabilized_scan_running = True), we will save the data each time we enter the convert_input method.
For now we will just try the saving of the scope spectra.

The method __init_saving_stabilized_scan prepare the h5 tree structure to welcome the saving of a stabilized scan. It also 





--- 02/02/21 ---

DAQ_Scan_Acquisition.init_data
------------------------------

In h5saver.add_data the init argument is set to True so it means that the array will be saved in the h5 file with correct type but all elements equals to zero.
Moreover the add_scan_dim argument is also set to True.

14h : it seems like it is working using CARRAY and not EARRAY !!! :D
-> h5saver.add_data(elargeable=False)

For the calibration scan: channel_array.shape should be a tuple (11, 502) because we have configured 11 steps of scan and the oscilloscope is configured with 500 samples.



Saving a stabilized scan
------------------------

We choose not to save the raw ROI since we will save the spectra from the oscilloscope.
-> BUT WE WILL HAVE TO SAVE THE ROIs BONDARIES AT SOME POINT !!!


PIDModel.det_done
-----------------

is this method ever called ??? -> yes it is triggered by the viewer module through the grab_done_signal in do_calibration.





--- 01/02/21 ---

Save data during the scan/Append an pytable array
-------------------------------------------------

To append an array of data at each step of the scan, it seems like we have to use the pytables __setitem__ method: https://www.pytables.org/usersguide/libref/homogenous_storage.html#tables.Array.__setitem__

It seems like it is what is done in DAQ_Scan_Acquisition.det_done.

h5saver.add_data
----------------

Is it necessary to give a channel_group as a parameter ? Couldn’t it be another type of group ?

EArray / CArray ?
-----------------

E seems to mean "enlargeable"

See : https://www.pytables.org/FAQ.html

CArray is for compressed array support. CArray are not enlargeable.
EArray is the most general array support. Compressible and enlargeable.

Workflow to save data during the scan
-------------------------------------

(inspired from DAQ_Scan)

(1) The (channel array) is initialized using h5saver.add_data at the first step of the scan (because it needs to know the shape of the data to initialize the array: See DAQ_Scan_Acquisition.det_done and DAQ_Scan_Acquisition.init_data).

What is the shape of data_dict that is sent as an argument in h5saver.add_data ??
-> dict(data=the_data_to_save)

(2) In the following steps we use the channel_array.__setitem__ method of the pytables library to fill the array. Remark: it seems like we could use channel_array[index] = value, but it seems quite confusing since it hides that the array we are dealing with is a pytable array and not a standard one…


Saving a stabilized scan
------------------------








--- 26/01/21 ---

Bug dans ellipses.fit
---------------------

Il faut bien sélectionner un nouveau fichier .h5 à chaque fois. Si on réécrit un ancien il semble que ça bug ??
Il semble plutôt que ce soit dû à la définition des ROIs qui donne une division par 0 ???

On a essayé en ajoutant ces lignes au début de ini_model (comme c’était le cas au commit d’avant) sans résultat :

        QtWidgets.QApplication.processEvents()
        QThread.msleep(500)
        QtWidgets.QApplication.processEvents()

C’est peut-être que le trigger du laser était tombé ?? -> non ça semble pas être ça non plus…

-> C’est la définition des ROIs qui merdait. Il faut utiliser la version 2 du fichier de définition des ROIs. Il donne des valeurs positives et loin de 0 pour tous les signaux.

What should be saved ?
----------------------

For the calibration scan what need to be saved is:
- the oscilloscope spectrum for each step
- the parameters of the ROIs
- the fitting ellipsis parameters

Node structure of the .h5 file
------------------------------

Should not we create the stabilized scans nodes as children of the calibration scan node ?
-> It seems to be a good idea since then it will be very easy to attribute a calibration scan to a stabilized scan.

Saving a stabilized scan
------------------------

At each step of the stabilized scan we should save:
- the time
- the value of the setpoint
- the value of the measured phase
- the value of the error
- the raw spectrum from the scope

This should be saved live, which means at each step those data should be written in the file.



--- 25/01/21 ---

Workflow
--------

* (0) Check communication with the piezo and the oscilloscope. We suppose to have optimized RABBIT conditions.
* (3) Configure the oscilloscope
	- in Sequence Mode with typically 500 sweeps averaging (2Hz) : if the acquisition frequency is too high, it may cause some desynchronization of the acquisition (see in the scope viewer) which is very bad for a feedback loop.
	- choose properly your window range, offset : once the oscilloscope module is initialized, do not touch the oscilloscope parameters ! You will probably have to restart the program if you do.
* (1) In a python IDE launch pymodaq/daq_utils/pid/pid_controller.py
* (2) In Parameters/Models class choose PIDModelLIZARD and click "Init model".
* (2bis) You will be asked to select (or create) a .h5 file where the data of the session will be saved.
* (4) Initialize the piezo and the oscilloscope modules. Check that you choose the correct channel. Start grabing.
* (5) Define 3 ROI (region of interest) as following:
	- click on the calculator icon on top of the scope viewer
	- click "Add" to add a new ROI. Define left/right positions, color, and Math type = Mean
	- ROI_00 should correspond to the first modulated signal M1. Typically sideband ??
	- ROI_01 corresponds to M2. Typically sideband ??
	- ROI_02 corresponds to the offset of the signal. Should be taken in a region where no electrons are detected. It is very important to respect those assignments otherwise the error signal cannot be properly calculated.
	- Once your ROIs are correctly defined click on "Save ROIs" and save the file somewhere so it will prevent you from doing the ROI definition next time by clicking on "Load ROIs".
* (6) Calibration
	- Go to Parameters/Models/Model params/Calibration/Calibration. Define start/stop positions (typically 2 microns range to get 10 oscillations) and step size (typically 20nm). The start position corresponding to your time zero.
	- Tick "Do calibration". At the end of the scan should appear in a different window on the left the ROIs values within the scanning range, on the right the corresponding XY representation and the ellipsis fit (green). At the end of the scan the delay stage should return to the starting position (time zero), the parameters of the fitting ellipsis should be set (Dx, Dy, x0, y0, phi) and the phase of the time zero.



--- 22/01/21 ---

H5Saver
-------

It seems that the closing of the h5 file created with h5saver.init_file is done in the method. So it probably not needed to take care of closing the file in the PIDModel.

On utilise

	h5saver.init_file(custom_naming=True)

pour qu’il ouvre une fenêtre popup pour que l’utilisateur renseigne le nom du fichier lors de l’initialisation du PID model.

On a commenté la ligne 172 du h5saver qui provoquait une erreur… Dans les versions ultérieures de pymodaq cette partie du code est modifiée.

Ça semble fonctionner comme ça on pourra donc supprimer les paramètres "Saving" dans le PID modèle.

Close h5 file
-------------

Apparemment la fermeture du fichier h5 avec h5saver.close_file() se fait plutôt à la fermeture de l’application (cf daq_scan_main.quit_fun()).

Si on ne ferme pas le fichier il n’est pas lisible avec HDFView.

Workflow h5 file
----------------

(1) At initialization of the application h5saver.init_file()
(2) Create nodes, save stuff,…
(3) At exit of the application h5saver.close_file()


--- 21/01/21 ---

Workflow
--------

(0) Check communication with the piezo and the oscilloscope. We suppose to have optimized RABBIT conditions.
(1) In a python IDE launch pymodaq/daq_utils/pid/pid_controller.py
(2) In Parameters/Models class choose PIDModelLIZARD
(3) Configure the oscilloscope
	- in Sequence Mode with typically 500 sweeps averaging (2Hz) : if the acquisition frequency is too high, it may cause some desynchronization of the acquisition (see in the scope viewer) which is very bad for a feedback loop.
	- choose properly your window range, offset : once the oscilloscope module is initialized, do not touch the oscilloscope parameters ! You will probably have to restart the program.
(4) Initialize the piezo and the oscilloscope modules. Check that you choose the correct channel. Start grabing.
(5) Define 3 ROI (region of interest) as following:
	- click on the calculator icon on top of the scope viewer
	- click "Add" to add a new ROI. Define left/right positions, color, and Math type = Mean
	- ROI_00 should correspond to the first modulated signal M1. Typically sideband ??
	- ROI_01 corresponds to M2. Typically sideband ??
	- ROI_02 corresponds to the offset of the signal. Should be taken in a region where no electrons are detected. It is very important to respect those assignments otherwise the error signal cannot be properly calculated.
	- Once your ROIs are correctly defined click on "Save ROIs" and save the file somewhere so it will prevent you from doing the ROI definition next time by clicking on "Load ROIs".
(6) Calibration
	- Go to Parameters/Models/Model params/Calibration/Calibration. Define start/stop positions (typically 2 microns range to get 10 oscillations) and step size (typically 20nm). The start position corresponding to your time zero.
	- Tick "Do calibration". At the end of the scan should appear in a different window on the left the ROIs values within the scanning range, on the right the corresponding XY representation and the ellipsis fit (green). At the end of the scan the delay stage should return to the starting position (time zero), the parameters of the fitting ellipsis should be set (Dx, Dy, x0, y0, phi) and the phase of the time zero.




egg-link
--------

It seems like if we do not install a package with the editing option, then any change we do on the files will not be taken into account will the program is running. Which means that we will have to restart the program after any change in the code, which can be very painful. (??)


Saving
------

The creation of the h5 file could be done while initializing the model ?

H5Saver test
------------

/Travail/Code/Python/pymodaq_h5_saver

It seems important to close the file

	h5_saver.close_file()


--- 20/01/21 ---

Pour le moment on travaille toujours dans l'environnement de base de Anaconda (C:\ProgramData\Anaconda3\...)

Test communication avec le piezo
--------------------------------

Avec le DAQ_Move PIezo_NI6215 : OK

(1) Brancher la sortie USB de la ALice Mariusz box
(2) Tourner le bouton sur le controller du piezo complètement counter-clockwise

Remarque : le DAQ_Move n'actualise pas la position affichée en temps réel. La position est actualisée à la fin du mouvement mais ensuite reste figée. Donc on suppose qu'il n'y a pas de fluctuation de la position entre les ordres... si on fait des mouvements relatifs par exemple ??

Test communication avec le scope
--------------------------------

DAQ_Viewer_1D
Scope parameters : Seq mode Averaging 10 sweeps -> trop rapide il semble qu'il freeze par moment.
	Averaging 500 sweeps : OK

On a utilisé le plugin LecroyWaverunner6ZiDom_TEST. Il n'y a pas de notes la-dessus mais il me semble qu'on avait un problème de synchronisation avec le plugin initial de Dominique à haute cadence et qu'on avait créé ce nouveau plugin qui résout le problème.

LIZARD Model
------------

On a :

PIDModelLIZARD
PIDModelLIZARD201005

Dans les deux cas le plugin Lecroy appelé est LecroyWaverunner6ZiDom_TEST donc pas de doute qu'il faut prendre celui-là.

Il semble que le PIDModelLIZARD est plus avancé puisqu'il y a l'attibut self.stabilized_scan_counter ??



Creation d'un dépot Github
--------------------------

On a suivi cette doc :

https://www.digitalocean.com/community/tutorials/how-to-push-an-existing-project-to-github

On a créé sur le compte Attolab un dépot privé (depuis /pymodaq_pid_models/models)

	pymodaq_LIZARD_FAB1

On a fait un

	git remote set-url origin

pour définir origin comme ce dépot (https://www.datree.io/resources/git-error-fatal-remote-origin-already-exists)


--- 19/01/21 ---

Emplacement pc central SE1, verion pymodaq
------------------------------------------

	C:\ProgramData\Anaconda3\Lib\site-packages\pymodaq

pas d'environnment particulier, on est dans l'environnement de base d'Anaconda.

La version de pymodaq est 1.6.3
Version python 3.7


Installation Anaconda + environnement python
--------------------------------------------

Sur le pc central on a fait une nouvelle installation de Anaconda qui se situe à :

	C:\Users\attose1\Anaconda3

le prompt Anaconda se situe à

	\condabin\conda.bat

On crée un environnement

	pymodaq_lizard

On installe la version 1.6.3 de pymodaq (la version avec laquelle on a développée initialement PIDModelLIZARD)

On fork le dépôt pymodaq_pid_models sur le compte github d'attolab.

On clone le dépot dans

	\attose1\pymodaq_github

Puis on utilise pip pour se mettre en mode édition

	cd \attose1\pymodaq_github\pymodaq_pid_models

	pip install -e .

Ce qui a créé un fichier

	pymodaq-pid-models.egg-link

dans \Anaconda3\envs\pymodaq_lizard\Lib\site-packages




--- 05/10/20 ---

On a eu un problème de connect() avec un signal parce qu'on a mis un '@' sur le décorateur de 'move done'

Move mirror before drilled mirror
---------------------------------

Joystick NEW FOCUS

DRIVER 1	Motor A 	vertical axis
		Motor B		horizontal axis

DRIVER 2 for drilled mirror



Filter
------

Enable filter should be False because it seems to prevent the piezo to move nicely...


Change parameters of the PID module (filter, output limits, PID constants...)
-----------------------------------

This is changed in ini_model method

PID parameter 'sample time'
---------------------------

??

PID parameters
--------------


Plutôt bonnes performances avec Kp =0.7 Ki =0.05 phase sign = +1



--- 02/10/20 ---

Output limits
-------------

It seems like those output limits are not used anywhere… we commented out the corresponding lines in ModelLIZARD.

Filter
------

??﻿


--- 01/10/20 ---

PID input/output viewers
------------------------

Pid input displays self.curr_input which is the measured phase extracted from the modulated signals.

Unwrap phase_buffer
-------------------

At each iteration, a phase within [-pi,+pi] is measured with get_phi_from_xy.
This phase is stored in phase_buffer.
We perform the unwrap operation on this list and get the last element.

This way we keep track of the history of the phase evolution. We can change the setpoint to value of phase that are out of [-pi,+pi]. Still we have the constraint that the change of setpoint should not be too large.


Phase time zero = phase offset
------------------------------

At the end of the calibration, the phase of the time zero (middle of the scan defined by the user) is calculated.
We will offset all the phases from phase_time_zero. This way the phase of the time zero becomes zero and becomes a better reference.







--- 30/09/20 ---

plantage lors d'une calibration (pid init + calibration)

move done
move done
move done
move done
move done
move done
move done
(-2147024882, 'E_OUTOFMEMORY', None, None)

Process finished with exit code -1073741819 (0xC0000005)



--- 29/09/20 ---

Offset piezo
------------

Il semble qu'il y ait toujours un offset de l'affichage sur le controlleur du piezo par rapport à la valeur affichée par pymodaq : le controlleur affiche +240nm par rapport à l'"affichage du soft.

Avant d'initialiser le piezo dans pymodaq il faut tourner le bouton couterclockwise et find home (cf dans les notes plus bas).

Sidebands
---------

Aujourdhui les sidebands sont là pour le piezo entre +30 et +35 microns envirion.

On sélectionne SB14 et SB20 comme signaux modulés. 


VIewer scope
------------

x from 6e-7 to 2.2e-6
y from 0.0018 to 0.007

On met le 'wait time' du scope à 0 ms. Sinon ilo semble qu'il se désynchronise à un moment..

ROI 1 (SB14) : 1.48e-6 -> 1.56e-6
ROI 2 (SB20) : 

Test do_calibration
-------------------

It seems to work but the ellipsis is not nice...
It seems like the piezo is going back to the central position at the end of the scan.
We have taken 3 different calibrations, the output parameters sounds quite similar. Sounds good.

Test launch pid
---------------

After calibration we tried to launch the close loop. It seems like it is well synchronized and measure something... but it does not order any movement to the piezo...

Il faut enlever 'Pause PID' pour envoyer des ordres au piezo !!

Test viewer scope
-----------------

Le problème de freezing de l'affichage du scope apparait aussi avec le simlple viewer de pymodaq...
Ca semble mieux marcher avec 

seq, avg = 2000 rafraichissement toutes les 2 sec environ


Last parameters
---------------

Kp = 5
Ki = 0.1
seq, avg = 2000

SB 14 et 20

Output limits are off




--- 04/08/20 ---

do_calibration
--------------

we would like the actuator to go back to the time zero at the end of the calibration scan.
It does not want to work… ??? The user will have to do it manually.


DAQ_PID l.703
-------------

                elif param.name() == 'set_point':
                    if self.pid_led.state:
                        self.command_pid.emit(ThreadCommand('update_options', dict(setpoint=param.value())))
                    else:
                        output = self.model_class.convert_output(param.value(),0, stab=False)
                        for ind_act, act in enumerate(self.actuator_modules):
                            act.move_Abs(output[ind_act])

???

If the setpoint is changed, and the pid is initialized, we update the setpoint of the pid module.

If the pid is not initialized, the parameter value is sent to convert_output and the actuator is moved ??!

Maybe the workflow should be different and the pid module should be initialized before doing the calibration ??


PIDRunner.output
----------------

This attribute is not clear…



--- 03/08/20 ---

Model.convert_output method
---------------------------

This method is used in DAQ_PID.parameter_tree_changed when one want to change the setpoint parameter.

	output = self.model_class.convert_output(param.value(),0,stab=False)

	actuator.move_Abs(output)

???

C’est pourquoi elle est appelée lorsqu’on initialise le modèle, au travers de setpoint_sb.setValue()





--- 31/07/20 ---

MockModelLIZARD
---------------

Les ROI ne sont pas pris tels quels. Ils sont normalisés par la constante de normalisation qui vaut environ 60. C'est pourquoi l'ellipse ne s'étend pas sur toute la plage des valeurs des ROIs.

get_phi_from_xy
---------------

On a modifié le calcul de phi et on a vérifié sur quelques exemples que ça semblait ok.
Les paramètres dans arctan2 sont plus simples que ce qui était mis dans le modèle Michelson. Il semble qu'on faisait deux fois la rotation…



--- 22/07/20 ---

Setpoint
--------

The setpoint set by the user should be the time delay with respect to the time zero.
When the user change the setpoint
- the pid should be stopped ? auto_mode = False
- we calculate the corresponding phase change \Delta \phi
- we take the modulus 2*\pi of the total phase (initial phase + \Delta \phi)
- the actuator is relatively moved with the corresponding displacement
- the rest is given as the new targeted phase (phase_target)



Changement de consigne
----------------------

On ne prévoit pas de changement de consigne supérieur à 2\pi pour le moment. C'est comme ça que c'est fait dans le programme de Martin. Ça veut dire qu'on n'a pas à arrêter le PID lors du changement de consigne puisque \Delta \phi est toujours inférieur à 2\pi.


Workflow
--------

- do_calibration -> parameters of the ellipse
- define time zero 	-> M1, M2 values
			-> get_phi_from_xy(M1,M2) to get the phase of time zero (phase_time_zero). Cette phase ne va pas changer tout au long de la stabilisation, jusqu'à ce qu'on fasse une nouvelle calibration.


--- 21/07/20 ---

Setpoint
--------

Le changement de setpoint est géré par DAQ_PID.parameter_tree_changed. Il envoie self.command_pid.emit(ThreadCommand('update_options'… au PIDRunner. Qui déclenche PIDRunner.set_option.


simple_pid auto_mode
--------------------

https://github.com/m-lundberg/simple-pid

To disable the PID so that no new values are computed, set auto mode to False.


Delay management/conventions
----------------------------

The positive direction of the piezo will reduce the dressing arm, so the dressing pulse will arrive sooner.
We consider the dressing pulse as the 'probe' and the XUV pulse as the 'pump'.

Following quite standard convention we define tau as positive if the probe (the IR) arrives on the sample after the pump (XUV pulse).

Set zero/Time zero definition
-----------------------------

When in RABBIT conditions, the user will have to define the Time zero, that is the conditions where he consider the pump and probe pulses are synchronized.
The time zero is typically at the center of the RABBIT scan/of the calibration scan.
At this point the user should click 'Set zero'.

If the variation of the piezo position \Delta l is positive, the variation of the pump-probe delay \Delta \tau is negative. There is a factor 2 because of the roundtrip of the light reflected from the moving mirror:

	\Delta \tau = - \frac{2\Delta l}{c}

Workflow
--------

Actually the definition of time zero should be done before launching the calibration scan. It should define by default the center of the calibration scan. Which means that the user should first click 'Set zero' or 'Define time zero' before clicking 'do_calibration'.





--- 20/07/20 ---

ModelLIZARD.phases
------------------

Constructed in interfero_from_phase.
It seems like phases will save all the measured phases from previous measurements.

The unwrap condition seems to be done on the phases list in interfero_from_phase.


interfero_from_phase/phase_offset
--------------------

the parameter phase_offset seems to be the targeted phase at which we should lock the interferometer.

The parameter interfero_offset ???

The parameter 'interfero_position' is updated at each iteration of the pid loop. It is calculated in interfero_from_phase. Its value is in microns in our case (same unit as the actuator). Its value is returned by convert_input, which means that it is send as the input of the pid module. Thus it should be the error from the targeted position ? Or the difference with the targeted position is done latter ?? Does the PID module take as input the error (current position - target) or the position ?

-> it seems like it takes the current position since the targeted position is sent has an argument (the pid module take an argument 'setpoint')

simple_pid
----------

Complete API documentation : https://simple-pid.readthedocs.io/en/latest/simple_pid.html#module-simple_pid.PID

It seems like DAQ_PID has no attribute pid. Only PIDRunner has such an attribute. Should be modified in the Attolab doc.

How/where is initialized this attribute ?

Initialization of the PID seems to start in DAQ_PID.ini_PID.
When PIDRunner is instanciated in ini_PID, the sixth argument sent is a dictionary with the parameters for the pid module (Kp, Ki, Kd, setpoint, sample_time, output_limits, auto_mode), which is called 'params' in the constructor.
IN the constructor of PIDRunner nothing fancy seems to happen.
So basically nothing particular in ini_PID...

PIDRunner.startPID
------------------

convert_output
--------------

The convert_output method should send an order in absolute value. THis ccan be seen in PIDRunner.start_PID.
For now it does nothing. It seems like it just transmit the output from the PID module directly as an order to the actuator (Absolute value).

interfero_offset
----------------

Where is contructed this guy ??

Initially its value is at zero (in the parameters of the model).
Its value can be set by the ModelLIZARD.update_settings method. Triggered if the user click 'Set zero'.

Set zero
--------

If the user click 'Set zero'
- phases will be cleared and become a list of a hundred zeros
- phase_offset -> curr_phase
- interfero_offset -> current actuator position in nm
- piezo_offset -> current actuator position in nm (NOT USED)

What is the difference between interfero_offset and piezo_offset parameters ??
-> in the current version of the code there is no difference. piezo_offset is not used at all...

It sounds strange that phase_offset is kept at zero after a 'Set zero'. curr_phase is kept at zero while get_phi_from_xy is not called. But this guy is called AFTER the stabization loop has been called... We would imagine that 'Set zero' should be called before launching the stabilization loop.. 


WORKFLOW
--------

Let say we have RABBIT conditions and have selected properly the ROIs.

(1) Click 'do_calibration'. (from 6 to 8)
(2) Go to say the central position of the calibration scan. (7)
(3) Here we want to stabilize at this position. Modify the 'Setpoint' (=7) so that it corresponds to the center of the calibration scan.
(4) Click 'set zero'.
	- phase_offset -> curr_phase
	- interfero_offset -> current actuator position (about 7)

curr_phase
----------

updated in get_phi_from_xy

get_phi_from_xy
---------------

Called by convert_input

interfero_phase
---------------

Does not seem to be used...
It is set in get_phi_from_xy at the same value as self.curr_phase








--- 17/07/20 ---

Correction appliquée à partir des ROI (LIZARDModel.convert_input)
-------------------------------------

Dans le programme de Martin, le calcul de la correction est effectué dans
	
	Feedback_loop.py

et peut-être un peu dans sideband_win.py

La 'condition unwrap' (qui détermine si on a changé de dent de scie) est effectuée avant le filtre PID.

Tout ça doit donc être effectué dans LIZARDModel.convert_input qui envoie une consigne au module externe PID.

Feedback_loop.py
----------------

self.data est construit par la méthode StoreData

ModelLIZARD
-----------

On doit sûrement normaliser les signaux dans do_calibration.

ROI_00 -> M1
ROI_01 -> M2
ROI_02 -> offset

To normalize the signals we need to get the complete signal at each iteration, which corresponds to the total number of electrons emitted, supposed to be independant of the pump-probe delay.

This is accessible through

	self.pid_controller.detector_modules[0].data_to_save_export['data1D']['CH000']['data']

which is a list of floats of size the number of samples (configured on the scope) which give the strength of the signal for each sample. Ce qui correspond à self.data[1] dans le prgramme de Martin (Feedback_loop.py).

On doit faire comme Martin :
	- retirer l'offset. Ce qu'il appelle data_without_BG.
	- intégrer le tout pour avoir la constante de normalisation qu'il appelle norm
	- diviser data_without_BG par norm pour obtenir shaped_data dont l'intégrale vaut 1.


ModelLIZARD.convert_input
-------------------------

argument : measurements

On peut accéder à ce qui est envoyé dans convert_input dans la méthode PIDRunner.start_PID. Appelé det_done_datas.

Pour accéder à la valeur d'un ROI

	det_done_datas['OSCILLOSCOPE']['data0D']['Measure_000']['data']


Il reste sûrement à faire la 'condition unwrap' ici.


Sauvegarde des ROI
------------------

Ne pas hésiter à utiliser l'option Save ROI une fois qu'ils ont été définis. Ca sauve un fichier qu'il suffit de loader la prochaine fois.




---16/07/20 ---

do calibration
--------------

Après avoir sélectionné deux ROI sur le viewer du scope on lance le programme en mode debug et on lance do calibration.
Il s'arrête l212 au moment où il boucle sur data_names qui est vide (exception).
Ca nous permet de vérifier que les valeurs des ROI sont bien stockées dans

	self.pid_controller.detector_modules[0].data_to_save_export['data0D']['Measure_000']['data']
pour le ROI_00 et dans
	self.pid_controller.detector_modules[0].data_to_save_export['data0D']['Measure_001']['data']
pour le ROI_01



On commente la ligne 212 'for ind_data, name in enumerate(self.data_names):'

A la place on met ça

                self.detector_data[ind_step, 0] = \
                self.pid_controller.detector_modules[0].data_to_save_export['data0D']['Measure_000']['data']
                # Measurement from ROI_01
                self.detector_data[ind_step, 1] = \
                self.pid_controller.detector_modules[0].data_to_save_export['data0D']['Measure_001']['data']

Lorsqu'on lance do calibration ça construit la liste self.detector_data qui contient pour chaque pas une liste de deux float qui sont les valeurs des deux ROI.


l224 self.viewer_calib.show_data affiche le résultat dans le viewer de gauche de la fenêtre 'Calibration'.

l228 self.viewer_ellipse est le viewer de droite



bug du plugin lecroy
--------------------

Il semble qu'il faut se mettre en mode sequence sur le scope pour que le plugin fonctionne correctement.
Il faut sélectionner la bonne voie avant d'initialiser le plugin.
SI jamais ça a planté il faut redémarrer le scope manuellement. Ou avec un script ? cf commentaires du plugin.


--- 15/07/20 ---

DEBUG module pycharm
--------------------

Pour utliser le DEBUG mode il suffit de lancer pid_controller.py en mode DEBUG (petit insect à coté de PLAY) après avoir mis des breakpoints dans les fichiers qui nous intéressent.
IL faut le faire dans le même projet pycharm.
Lorsque le programme s'arrête à un breakpoint, l'onglet pycharm devient orange.
Il semble que le mode DEBUG ne fonctionne pas si une erreur survient dans le logger de pycharm.

Quand on a atteint un breakpoint on peut accéder aux variables dans l'onglet DEBUGGER (en bas de la fenêtre), onglet VARIABLES.

DEBUG LIZARDModel
-----------------

LIZARDModel

	l.212 data_names
	-> construit par PIDGeneric.update_detector_names
	-> et update_detector_names est appelé par DAQ_PID.parameter_tree_changed quand on modifie le paramètre 'detector_modules'. Paramètre qui n'existe pas !!!


L'erreur qui apparait dans le logger pymodaq vient de la ligne 98 dans LIZARDMdel

	-> on a commenté cette ligne

On obtient une autre erreur 'DAQ_Viewer object has no attribute 'Initialized state' qui doit venir de la ligne 106 dans LIUZARDModel

	-> on ne doit pas entrer dans la condition et donc ne pas enclencher 'grab_data'
	-> on commente cette condition

Nouvelle erreur dans le logger 'Parameter main_settings has no child named update_modules'
	-> cette erreur doit venir de la ligne 112


l117 : self.pid_controller.settings.child('main_settings', 'detector_modules').value().copy() ??
	-> de même où est ce paramètre ?


Par contre 'detector_modules' est un attribut de DAQ_PID...



--- 10/07/20 ---

Dans PIDModelGeneric

	self.pid_controller.settings.child('main_settings', 'detector_modules')

pid_controller instance de DAQ_PID. Mais où est le paramètre 'detector_modules' ??

self.data_names est construit dans PIDModelGeneric.update_detector_names

update_detector_names est appelé dans DAQ_PID.parameter_tree_changed

PIDModelLIZARD premier test
---------------------------

La communication avec le scope et le piezo est OK !

On a une erreur 'in pid_controller.py method ini_model line 619: 'Ui_Form has no attribute roiBtn''

In the scope viewer click to 'Do Math' (icone calculette)

Add ROI : dans le paramètre 'Use channel' on ne peut sélectionner que CH0... ? En fait ça semble correspondre
à la voie qui est affichée, il suffit de mettre les bonnes bornes pour le ROI

On a sélectionné deux ROI (voir capture d'écran).

Si on coche 'Do calibration' dans les paramètres ça fait planter le programme... Dans la console est affiché 'move done', le piezo est bien allé à la première valeur du scan de calibration mais ensuite ça plante sans afficher rien d'autre 'Process finished with exit code...'

Les paramètres du modèle sont accessibles dans le widget PID controller. On suppose qu'ils apparaissent lors du chargement du modèle...

Quand on fait un find home avec le piezo il arrive à 27.9 um... il semble que les mouvements sont relatifs à cettte position.

-> il faut vérifier que la commande manuelle du piezo soit à zero : bouton qui tourne à mettre à fond vers la gauche (counter-clockwisde). Dans ces conditions il semble réagir correctement. Le find home va bien à zero et les mouvements relatifs et absolus fonctionnent. Par contre même pour epsilon=5nm il semble qu'il valide des positions en dehors de cet intervalle ce qui est assez bizarre... On dirait que la précision maximale est de 10nm...




--- 09/07/20 ---

path pc central
C:/ProgramData/Anaconda3/Lib/site-packages/pymodaq/...

Le dossier ProgramData est caché

Le nom du module pour commander le piezo de FAB1 est

	daq_move_Piezo_NI6215

Le nom du module pour l'acquisition du scope est

	daq_1Dviewer_LecroyWaverunner6ZiDom
