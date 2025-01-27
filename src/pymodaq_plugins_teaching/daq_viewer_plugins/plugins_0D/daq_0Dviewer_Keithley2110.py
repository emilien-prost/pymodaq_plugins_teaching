import numpy as np
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, DataToExport, Axis
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.parameter import Parameter
from time import perf_counter

from pymodaq_plugins_teaching.hardware.keithley import Keithley2110

# TODO:
# (1) change the name of the following class to DAQ_0DViewer_TheNameOfYourChoice
# (2) change the name of this file to daq_0Dviewer_TheNameOfYourChoice ("TheNameOfYourChoice" should be the SAME
#     for the class name and the file name.)
# (3) this file should then be put into the right folder, namely IN THE FOLDER OF THE PLUGIN YOU ARE DEVELOPING:
#     pymodaq_plugins_my_plugin/daq_viewer_plugins/plugins_0D
class DAQ_0DViewer_Keithley2110(DAQ_Viewer_base):
    """ Instrument plugin class for a OD viewer.

    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Viewer module through inheritance via
    DAQ_Viewer_base. It makes a bridge between the DAQ_Viewer module and the Python wrapper of a particular instrument.


    TODO Complete the docstring of your plugin with:
        * The set of instruments that should be compatible with this instrument plugin.
        * With which instrument it has actually been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.

    # TODO add your particular attributes here if any

    """
    params = comon_parameters + [
        ## TODO for your custom plugin: elements to be added here as dicts in order to control your custom stage
    ]

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        self.controller: Keithley2110 = None  #Ici le ":" est du typing "tu peux t'attendre à ce que l'objet soit de type Keithley2110"
        # faire le typing permets d'avoir l'autocomplétion dans la suite

        # TODO declare here attributes you want/need to init with a default value
        pass

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == "a_parameter_you've_added_in_self.params":
            self.controller.your_method_to_apply_this_param_change()  # when writing your own plugin replace this line

    #        elif ...
    ##

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        # raise NotImplemented  # TODO when writing your own plugin remove this line and modify the one below
        self.ini_detector_init(old_controller=controller,
                               new_controller=Keithley2110())  # new_controller devient une instance de classe Keithley2110
                                # et appel la fonction init de la classe
        self.controller.open_communication('USB::120x::RAW')

        # TODO for your custom plugin (optional) initialize viewers panel with the future type of data
        # self.dte_signal_temp.emit(DataToExport(name='myplugin',
        #                                        data=[DataFromPlugins(name='Mock1',
        #                                                              data=[np.array([0]), np.array([0])],
        #                                                              dim='Data0D',
        #                                                              labels=['Mock1', 'label2'])]))

        info = "Whatever info you want to log"
        initialized = self.controller.is_open  # TODO
        return info, initialized  # si erreur de communication retourne une erreur

    def close(self):
        """Terminate the communication protocol"""
        ## TODO for your custom plugin
        self.controller.close()  # when writing your own plugin replace this line

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        ## TODO for your custom plugin: you should choose EITHER the synchrone or the asynchrone version following

        # synchrone version (blocking function)
        # raise NotImplemented  # when writing your own plugin remove this line
        Nbuffer = 20
        data_tot = []
        time = []
        start_time = perf_counter()
        for _ in range(Nbuffer):
            data_tot.append(self.controller.get_reading())
            time.append(perf_counter()-start_time)

        data_array = np.array(data_tot)
        mean = np.array([data_array.mean()])
        time_array = np.array(time)

        # data_tot = self.controller.get_reading() # to get one value is this line
        self.dte_signal.emit(DataToExport(name='myplugin',
                                          data=[DataFromPlugins(name='Buffer', data=[data_array],
                                                                dim='Data1D', labels=['volt'],
                                                                axes=[Axis(label='Time', units='s', data=time_array)
                                                                      ]
                                                                ),
                                                DataFromPlugins(name='Mean', data=[mean],
                                                                dim='Data0D', labels=['mean'])
                                                ]
                                          )
                             )

        #########################################################

        # # asynchrone version (non-blocking function with callback)
        # raise NotImplemented  # when writing your own plugin remove this line
        # self.controller.your_method_to_start_a_grab_snap(
        #     self.callback)  # when writing your own plugin replace this line
        #########################################################

    def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        data_tot = self.controller.your_method_to_get_data_from_buffer()
        self.dte_signal.emit(DataToExport(name='myplugin',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data0D', labels=['dat0', 'data1'])]))

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        ## TODO for your custom plugin
        # raise NotImplemented  # when writing your own plugin remove this line
        # self.controller.reset()  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))
        ##############################
        return ''


if __name__ == '__main__':
    main(__file__)