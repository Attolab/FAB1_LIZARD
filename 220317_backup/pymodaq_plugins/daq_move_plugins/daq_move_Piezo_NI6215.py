from pymodaq.daq_move.utility_classes import DAQ_Move_base
from pymodaq.daq_move.utility_classes import comon_parameters
from pymodaq.daq_utils.daq_utils import ThreadCommand
from pymodaq.daq_utils.custom_parameter_tree import iter_children
from easydict import EasyDict as edict

import nidaqmx
import time


class DAQ_Move_Piezo_NI6215(DAQ_Move_base):
    """
     Template to be used in order to write your own Move modules

    """
    _controller_units = 'um'  # dependent on the stage type so to be updated accordingly when/if needed
    #  using self.controller_units = new_unit
    # define here the default values you need for the hardware settings

    # To be set to True (default is false in base class) if your controller controls multiple axis and then must be initialized only once (see Preset Mode documentation)
    is_multiaxes = False
    stage_names = ['X']  # any names that are relevant with you controller axes
    # list of dictionnaries defining the hardware parameters one want available in the UI
    params = [  # custom list below is just an example
                 {'title': 'group parameter:', 'name': 'group_parameter', 'type': 'group', 'children': [
                     {'title': 'Controller Name:', 'name': 'controller_name', 'type': 'str',
                      'value': 'actuator controller', 'readonly': True},
                     {'title': 'Controller address:', 'name': 'controller_address', 'type': 'int', 'value': 1,
                      'default': 1, 'min': 1},
                 ]},

                 ##########################################################
                 # the ones below should ALWAYS be present!!!
                 {'title': 'MultiAxes:', 'name': 'multiaxes', 'type': 'group', 'visible': is_multiaxes, 'children': [
                     {'title': 'is Multiaxes:', 'name': 'ismultiaxes', 'type': 'bool', 'value': is_multiaxes,
                      'default': False},
                     {'title': 'Status:', 'name': 'multi_status', 'type': 'list', 'value': 'Master',
                      'values': ['Master', 'Slave']},
                     {'title': 'Axis:', 'name': 'axis', 'type': 'list', 'values': stage_names},

                 ]}] + comon_parameters

    ##########################################################
    def __init__(self, parent=None, params_state=None):
        # modify the name here as your plugin name
        super(DAQ_Move_Piezo_NI6215, self).__init__(parent, params_state)
        self.settings.child(('epsilon')).setValue(5)  # same value as in the Labview program

        self.um_min = 0.0
        self.um_max = 72.05
        self.V_max = 9.955
        self.V_min = 0.0033

        # wahtever has to be initialized here (not yet the controller but it could be the loading of the dll, wrapper...
        try:
            # set the bound options to True (present in common_parameters)
            self.settings.child('bounds', 'is_bounds').setValue(True)
            self.settings.child('bounds', 'min_bound').setValue(self.um_min)
            self.settings.child('bounds', 'max_bound').setValue(self.um_max)

        except Exception as e:
            self.emit_status(ThreadCommand("Update_Status", [str(e)]))
            raise Exception(str(e))

    def V2um(self, V):
        return (V - self.V_min) / (self.V_max - self.V_min) * (self.um_max - self.um_min) + self.um_min

    def um2V(self, um):
        return (um - self.um_min) / (self.um_max - self.um_min) * (self.V_max - self.V_min) + self.V_min

    def DV2Dum(self, V):
        return V / (self.V_max - self.V_min) * (self.um_max - self.um_min)

    # Vread = 0.9953*Vwrite + 0.0033
    def V_real(self, V):
        return (V - 0.0033) / 0.9953

    def check_position(self):
        """
            Get the current hardware position with scaling conversion given by get_position_with_scaling.
        """

        # get actuator value ("position") from controller
        # for instance, fake method
        task = nidaqmx.Task()
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        ai = task.ai_channels[0]
        ai.ai_rng_high = 10.0
        pos = self.V2um(task.read())
        task.close()
        # task.__exit__(None, None, None)

        # convert pos if scaling options have been used, mandatory here
        # pos = self.get_position_with_scaling(pos)
        self.current_position = pos
        self.emit_status(ThreadCommand('check_position', [pos]))
        return pos

    def close(self):
        """
            close the current instance of instrument.
        """
        pass

    def commit_settings(self, param):
        """
        Activate parameters changes on the hardware.
        """

        # here we update the hardware if parameters have been changed by the user

        # for instance:

        if param.name() == 'conex_lib':
            # then init the dll on the new path defined by the parameter value
            # for instance call the update_dll method of the controller object, fake here:
            self.controller.update_dll(param.value())

        # here check if the name of the parameter is a child of the group_parameter parameter
        # the group_parameter is obtained from self.settings using the child method
        # iter_children returns a list of all parameter names that are children or subchildren of 'group_parameter'
        elif param.name() in iter_children(self.settings.child('group_parameter'), childlist=[]):
            # then do something on self.controller or something else!
            pass

    def ini_stage(self, controller=None):
        """
            Initialize the controller and stages (axes) with given parameters.

            =============== ================================================ =========================================================================================
            **Parameters**   **Type**                                         **Description**
            *controller*     instance of the specific controller object       If defined this hardware will use it and will not initialize its own controller instance
            =============== ================================================ =========================================================================================

            Returns
            -------
            Easydict
                dictionnary containing keys:
                 * *info* : string displaying various info
                 * *controller*: instance of the controller object in order to control other axes without the need to init the same controller twice
                 * *stage*: instance of the stage (axis or whatever) object
                 * *initialized*: boolean indicating if initialization has been done correctly

            See Also
            --------
            DAQ_utils.ThreadCommand
        """
        try:
            # initialize the stage and its controller status
            # controller is an object that may be passed to other instances of DAQ_Move_Actuator in case
            # of one controller controlling multiaxes
            self.status.update(edict(info="", controller=None, initialized=False))

            # check whether this stage is controlled by a multiaxe controller (to be defined for each plugin)
            # if mutliaxes then init the controller here if Master state otherwise use external controller
            if self.settings.child('multiaxes', 'ismultiaxes').value() and self.settings.child('multiaxes',
                                                                                               'multi_status').value() == "Slave":
                if controller is None:
                    raise Exception('no controller has been defined externally while this axe is a slave one')
                else:
                    self.controller = controller
            else:  # Master stage
                pass
            # self.status.controller = self.controller
            self.status.initialized = True

            return self.status

        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status', [str(e), 'log']))
            self.status.info = str(e)
            self.status.initialized = False
            return self.status

    def move_Abs(self, position):
        """
        Move to an absolute position
        """
        # limit position if bounds options has been selected and if position is out of them
        position = self.check_bound(position)
        self.target_position = position
        # convert the user set position to the controller position if scaling has been activated by user
        position = self.set_position_with_scaling(position)

        task = nidaqmx.Task()
        task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
        task.write(self.V_real(self.um2V(position)))
        task.close()
        # task.__exit__(None, None, None)

        # start polling the position until the actuator reach the target position within epsilon (defined as a parameter field (comon_parameters)
        self.poll_moving()
        print('move done')

    def move_Rel(self, position):
        """
        Move to a relative position
        """
        # limit position if bounds options has been selected and if position is out of them
        position = self.check_bound(self.current_position + position) - self.current_position
        self.target_position = position + self.current_position
        # convert the user set position to the controller position if scaling has been activated by user
        position = self.set_position_relative_with_scaling(position)

        # set relative motion position, for instance (fake method):
        self.move_Abs(self.target_position)



    def move_Home(self):
        """
        Move to home: could be a switch or a limit.somtetimes this is not available
        """

        self.move_Abs(0)
        # or if not available
        self.emit_status(ThreadCommand('Update_Status', ['Move Home not implemented/available']))

    def stop_motion(self):
        """
            See Also
            --------
            DAQ_Move_base.move_done
        """
        # for instance, fake method

        self.move_done()
