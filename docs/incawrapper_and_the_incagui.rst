Using the INCAWrapper and the INCA GUI
================================================================================

Though it is possible to use the INCAWrapper completely independent of the INCA GUI, there can be good reasons to use the INCA GUI combined with the INCAWrapper. For example, to manually verify that the model is setup as intended or run and diagnose the model. It is possible to open, modify and run the models that were created using the INCAWrapper in the INCA GUI. It is also possible to export the results from runs done through the GUI. However, it is not possible to export a INCAScript or the input data in the correct structure for the INCAWrapper from the INCA GUI.


Opening models created with the INCAWrapper in the INCA GUI
--------------------------------------------------------------------------------
The function ``run_inca`` produce a .mat file that can be opened in the INCA GUI. This is done by selecting the *Open Model* or *Open Flux Map* in the INCA GUI. INCA will fail to open flux maps, i.e. results of an estimation algorithm, if the .mat files does not contain a simulation. Therefore, the argument ``run_simulation=True`` (default) must be used when calling ``define_runner()`` function.



**Monte Carlo Results cannot be opened in the INCA GUI**

At the moment, the INCAWrapper does not save Monte Carlo results in a format that can be read by the INCA GUI. Thus, results of Monte Carlo simulations done through the INCAWrapper can only be opened through the INCAWrapper.


Saving models and estimation runs from the INCA GUI
--------------------------------------------------------------------------------
The INCA GUI has several save options. The different options saves different data along with the model. All options saves a .mat file that can be read by the INCAWrapper using the the ``INCAResults`` class. The options are:

* Save Model as: Saves only the model with the current settings.
* Save Flux Map as: Saves the model and the results of the the estimation algorithm that was most recently run.
* Save Simulation as: [Import into INCAWrapper is not implemented] Saves the model and the results of the simulation that was most recently run.