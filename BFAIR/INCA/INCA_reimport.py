# -*- coding: utf-8 -*-
"""Data re-import module."""

import time
from math import isnan, isinf
import re
from molmass.molmass import Formula
import scipy.io
import os
import pandas as pd
from datetime import datetime
from stat import ST_SIZE, ST_MTIME

__version__ = "0.0.1"


class INCA_reimport:
    def __init__(self):
        self.fittedData = pd.DataFrame()
        self.fittedFluxes = pd.DataFrame()
        self.fittedFragments = pd.DataFrame()
        self.fittedMeasuredFluxes = pd.DataFrame()
        self.fittedMeasuredFragments = pd.DataFrame()
        self.fittedMeasuredFluxResiduals = pd.DataFrame()
        self.fittedMeasuredFragmentResiduals = pd.DataFrame()
        self.simulationParameters = pd.DataFrame()

    def extract_file_info(self, filename):
        """
        Extracts information about the file

        Parameters
        ----------
        filename: str
            name of the .mat file we want to get information about

        Returns
        -------
        info: dict
            a dict containing the file information, its size,
            the structure of the timestamp
            and the timestamp of when the simulation was run
        """
        try:
            st = os.stat(filename)
        except IOError:
            print("failed to get information about", filename)
            return
        else:
            file_size = st[ST_SIZE]
            simulation_dateAndTime_struct = time.localtime(st[ST_MTIME])
            simulation_dateAndTime = datetime.fromtimestamp(
                time.mktime(simulation_dateAndTime_struct)
            )
            info = {
                "File_size": file_size,
                "Simulation_timestamp_structure": simulation_dateAndTime_struct,
                "Simulation_timestamp": simulation_dateAndTime,
            }
        return info

    def det_simulation_type(self, simulation_info):
        """
        Determine if the simulation is a parallel labeling
        experiment, non-stationary, or both

        Parameters
        ----------
        simulation_info: pandas.DataFrame
            The MS fragment file corresponding
            to the simulation

        Returns
        -------
        parallel: bool
        non_stationary: bool
            booleans that describe the type
            of experiment that was simulated
        """
        parallel = False
        non_stationary = False
        if (
            len(simulation_info["experiment_id"]) > 1
            or len(simulation_info["sample_name_abbreviation"]) > 1
        ):
            parallel = True
        if len(simulation_info["time_point"]) > 1:
            non_stationary = True
        return parallel, non_stationary

    def data_extraction(self, filename):
        """
        Extract simulation data

        Parameters
        ----------
        filename: str
            name of the .mat file we want to get information about

        Returns
        -------
        m: scipy.MatlabObject
            the model used for the simulation
        f: scipy.MatlabObject
            the fit of the model
        """
        m = scipy.io.loadmat(filename)["m"]  # model
        f = scipy.io.loadmat(filename)["f"]  # fitdata
        # s = scipy.io.loadmat(filename)['s']  # simdata, not used here
        return m, f

    def extract_model_info(self, m):
        """
        Extract model information

        Parameters
        ----------
        m: scipy.MatlabObject
            the model extracted from the file

        Returns
        -------
        model_info: pandas.DataFrame
            a DataFrame containing the MS id,
            the id of the experiment and a boolean
            describing which experiments were used in the model
        """
        m_ms_expt = []
        m_ms_id = []
        m_ms_on = []
        for exp in m["expts"]:
            exp_id = exp[0][0]["id"][0][0]
            for d in exp[0][0]["data_ms"][0]["id"][0]:
                m_ms_expt.append(exp_id)
                m_ms_id.append(d[0])
                m_ms_on.append(bool(d[0][0]))
        model_info = {"Exp": m_ms_expt, "MS_id": m_ms_id, "Exp_used": m_ms_on}
        model_info = pd.DataFrame.from_dict(model_info, "index")
        return model_info

    def extract_sim_params(self, simulation_id, info, m, filename):
        """
        Extract simulation parameters

        Parameters
        ----------
        simulation_id: str
            The name of the experiment used for
            the simulation as in the MS frament file
        m: scipy.MatlabObject
            the model extracted from the file
        filename: str
            name of the .mat file we want to get information about

        Returns
        -------
        simulationParameters: pandas.DataFrame
            the simulation parameters
        """
        simulation_dateAndTime = info["Simulation_timestamp"]
        m_options = {
            "cont_alpha": float(m["options"][0][0][0]["cont_alpha"][0][0][0]),
            "cont_reltol": float(
                m["options"][0][0][0]["cont_reltol"][0][0][0]
            ),
            "cont_steps": float(m["options"][0][0][0]["cont_steps"][0][0][0]),
            "fit_nudge": float(m["options"][0][0][0]["fit_nudge"][0][0][0]),
            "fit_reinit": bool(m["options"][0][0][0]["fit_reinit"][0][0][0]),
            "fit_reltol": float(m["options"][0][0][0]["fit_reltol"][0][0][0]),
            "fit_starts": float(m["options"][0][0][0]["fit_starts"][0][0][0]),
            "fit_tau": float(m["options"][0][0][0]["fit_tau"][0][0][0]),
            "hpc_on": bool(m["options"][0][0][0]["hpc_on"][0][0][0]),
            "int_maxstep": float(
                m["options"][0][0][0]["int_maxstep"][0][0][0]
            ),
            "int_reltol": float(m["options"][0][0][0]["int_reltol"][0][0][0]),
            "int_senstol": float(
                m["options"][0][0][0]["int_senstol"][0][0][0]
            ),
            "int_timeout": float(
                m["options"][0][0][0]["int_timeout"][0][0][0]
            ),
            "int_tspan": float(m["options"][0][0][0]["int_tspan"][0][0][0]),
            "ms_correct": bool(m["options"][0][0][0]["ms_correct"][0][0][0]),
            "oed_crit": m["options"][0][0][0]["oed_crit"][0][0],
            "oed_reinit": bool(m["options"][0][0][0]["oed_reinit"][0][0][0]),
            "oed_tolf": float(m["options"][0][0][0]["oed_tolf"][0][0][0]),
            "oed_tolx": float(m["options"][0][0][0]["oed_tolx"][0][0][0]),
            "sim_more": bool(m["options"][0][0][0]["sim_more"][0][0][0]),
            "sim_na": bool(m["options"][0][0][0]["sim_na"][0][0][0]),
            "sim_sens": bool(m["options"][0][0][0]["sim_sens"][0][0][0]),
            "sim_ss": bool(m["options"][0][0][0]["sim_ss"][0][0][0]),
            "sim_tunit": [m["options"][0][0][0]["sim_tunit"][0][0]],
        }
        try:
            m_options.update(
                {"hpc_mcr": m["options"][0][0][0]["hpc_mcr"][0][0]}
            )
        except ValueError:
            m_options.update(
                {"hpc_mcr": float(m["options"][0][0][0]["hpc_bg"][0][0][0])}
            )
        try:
            m_options.update(
                {"hpc_serve": m["options"][0][0][0]["hpc_serve"][0][0]}
            )
        except ValueError:
            m_options.update(
                {"hpc_serve": m["options"][0][0][0]["hpc_sched"][0][0]}
            )
        m_options.update(
            {
                "simulation_id": simulation_id,
                "simulation_dateAndTime": simulation_dateAndTime,
                "original_filename": filename,
                "used_": True,
                "comment_": None,
            }
        )
        simulationParameters = pd.DataFrame.from_dict(m_options)
        return simulationParameters

    def extract_base_stats(self, f, simulation_id, info):
        """
        Extract fit information

        Parameters
        ----------
        f: scipy.MatlabObject
            the fit of the model
        simulation_id: str
            The name of the experiment used for the
            simulation as in the MS frament file
        info: dict
            output of the "extract_file_info(filename)" function

        Returns
        -------
        fittedData: pandas.DataFrame
            base statistics describing the fit
        """
        f_Echi2 = None
        simulation_dateAndTime = info["Simulation_timestamp"]
        if not isnan(f["Echi2"][0][0][0][0]):
            if len(f["Echi2"][0][0][0]) > 1:
                f_Echi2 = [f["Echi2"][0][0][0][0], f["Echi2"][0][0][0][1]]
            else:
                f_Echi2 = [f["Echi2"][0][0][0][0]]
        f_alf = f["alf"][0][0][0][0]
        f_chi2 = f["chi2"][0][0][0][0]
        f_dof = int(f["dof"][0][0][0][0])
        f_ = {
            "fitted_echi2": f_Echi2,
            "fitted_alf": f_alf,
            "fitted_chi2": f_chi2,
            "fitted_dof": f_dof,
        }
        f_.update(
            {
                "simulation_id": simulation_id,
                "simulation_dateAndTime": simulation_dateAndTime,
                "used_": True,
                "comment_": None,
            }
        )
        fittedData = pd.DataFrame.from_dict(f_)
        return fittedData

    def get_fit_info(self, f):
        """
         Extract information and sum of the squared residuals of
         the fitted measurements

         Parameters
         ----------
         f: scipy.MatlabObject
             the fit of the model

        Returns
        -------
         f_mnt_info: dict
             a dict containing the the reaction id of the fitted
             measurements, the sum of the squared residuals,
             the id of the experiment used for the simulation
             and the type of the current value (a measured flux or an
             MS measurement)
        """
        f_mnt_id = []
        f_mnt_sres = []
        f_mnt_expt = []
        f_mnt_type = []  # Flux or MS
        for d in f["mnt"][0][0][0]["id"]:
            f_mnt_id.append(d[0])
        for d in f["mnt"][0][0][0]["sres"]:
            f_mnt_sres.append(float(d[0][0]))
        for d in f["mnt"][0][0][0]["expt"]:
            f_mnt_expt.append(d[0])
        for d in f["mnt"][0][0][0]["type"]:
            f_mnt_type.append(d[0])
        f_mnt_info = {
            "rxn_id": f_mnt_id,
            "rss": f_mnt_sres,
            "expt_name": f_mnt_expt,
            "expt_type": f_mnt_type,
        }
        return f_mnt_info

    # Only works for single experiments for now, might have to change it
    # for parallel labeling
    def sort_fit_info(self, f_mnt_info, simulation_info, fittedData):
        """
        Seperate the information from the original input, the "get_fit_info(f)"
        function, the "extract_file_info(filename)" function and the
        "extract_base_stats(f, simulation_id, info)" function
        into appropriate rows

        Parameters
        ----------
        f_mnt_info: dict
            the output of the "get_fit_info(f)" function
        simulation_info: pandas.DataFrame
            The MS fragment file corresponding to the simulation
        fittedData: pandas.DataFrame
            the output of the "extract_base_stats(f, simulation_id, info)"
            function

        Returns
        -------
        fittedMeasuredFluxes: pandas.DataFrame
            info about the fluxes used as an input
            for the simulation
        fittedMeasuredFragments: pandas.DataFrame
            info about the MS data used as an
            input for the simulation
        """
        fittedMeasuredFluxes = {}
        fittedMeasuredFragments = {}
        rxn_id = f_mnt_info["rxn_id"]
        rss = f_mnt_info["rss"]
        expt_name = f_mnt_info["expt_name"]
        expt_type = f_mnt_info["expt_type"]
        simulation_id = fittedData["simulation_id"].unique()[0]
        simulation_dateAndTime = fittedData["simulation_dateAndTime"].unique()[
            0
        ]
        for cnt, x_type in enumerate(expt_type):
            if x_type == "Flux":
                if expt_name[cnt] in list(simulation_info["experiment_id"]):
                    fittedMeasuredFluxes[cnt] = {
                        "simulation_id": simulation_id,
                        "simulation_dateAndTime": simulation_dateAndTime,
                        "experiment_id": expt_name[cnt],
                        "sample_name_abbreviation": simulation_info[
                            "sample_name_abbreviation"
                        ][0],
                        "rxn_id": rxn_id[cnt],
                        "fitted_sres": rss[cnt],
                        "used_": True,
                        "comment_": None,
                    }
                elif expt_name[cnt] in list(
                    simulation_info["sample_name_abbreviation"]
                ):
                    fittedMeasuredFluxes[cnt] = {
                        "simulation_id": simulation_id,
                        "simulation_dateAndTime": simulation_dateAndTime,
                        "experiment_id": simulation_info["experiment_id"][0],
                        "sample_name_abbreviation": expt_name[cnt],
                        "rxn_id": rxn_id[cnt],
                        "fitted_sres": rss[cnt],
                        "used_": True,
                        "comment_": None,
                    }
            elif x_type == "MS":
                if expt_name[cnt] in list(simulation_info["experiment_id"]):
                    fittedMeasuredFragments[cnt] = {
                        "simulation_id": simulation_id,
                        "simulation_dateAndTime": simulation_dateAndTime,
                        "experiment_id": expt_name[cnt],
                        "sample_name_abbreviation": simulation_info[
                            "sample_name_abbreviation"
                        ][0],
                        "fragment_id": rxn_id[cnt],
                        "fitted_sres": rss[cnt],
                        "used_": True,
                        "comment_": None,
                    }
                elif expt_name[cnt] in list(
                    simulation_info["sample_name_abbreviation"]
                ):
                    fittedMeasuredFragments[cnt] = {
                        "simulation_id": simulation_id,
                        "simulation_dateAndTime": simulation_dateAndTime,
                        "experiment_id": simulation_info["experiment_id"][0],
                        "sample_name_abbreviation": expt_name[cnt],
                        "fragment_id": rxn_id[cnt],
                        "fitted_sres": rss[cnt],
                        "used_": True,
                        "comment_": None,
                    }
            else:
                print("type not recognized")
        fittedMeasuredFluxes = pd.DataFrame.from_dict(
            fittedMeasuredFluxes, "index"
        )
        fittedMeasuredFragments = pd.DataFrame.from_dict(
            fittedMeasuredFragments, "index"
        )
        return fittedMeasuredFluxes, fittedMeasuredFragments

    def get_residuals_info(self, f, simulation_info):
        """
        Extract the residuals of the fitted measurements

        Parameters
        ----------
        f: scipy.MatlabObject
            the fit of the model
        simulation_info: pandas.DataFrame
            The MS fragment file corresponding to
            the simulation

        Returns
        -------
        f_mnt_res_info: dict
            a dict containing the residuals of the fit,
            the fit itself, the type of the current value (a measured flux
            or an MS measurement)
            reaction id of the fitted measurements, the standard
            deviation of the fit,
            the time point of the sample, the name of the expeiment,
            the data used for the fit, the peak of the residuals
        """
        f_mnt_res_val = []
        f_mnt_res_fit = []
        f_mnt_res_type = []  # Flux or MS
        f_mnt_res_id = []
        f_mnt_res_std = []
        f_mnt_res_time = []
        f_mnt_res_expt = []
        f_mnt_res_data = []
        f_mnt_res_peak = []
        for d in f["mnt"][0][0][0]["res"]:
            f_mnt_res_val.append(float(d[0][0]["val"][0][0]))
            f_mnt_res_fit.append(float(d[0][0]["fit"][0][0]))
            f_mnt_res_type.append(d[0][0]["type"][0])
            f_mnt_res_id.append(d[0][0]["id"][0])
            f_mnt_res_std.append(float(d[0][0]["std"][0][0]))
            # change default of time inf to 0
            if isinf(d[0][0]["time"][0][0]):
                f_mnt_res_time.append("0")
            else:
                f_mnt_res_time.append(str(d[0][0]["time"][0][0]))
            if d[0][0]["expt"][0] == "Expt #1":
                f_mnt_res_expt.append(simulation_info["experiment_id"][0])
            else:
                f_mnt_res_expt.append(d[0][0]["expt"][0])
            f_mnt_res_data.append(d[0][0]["data"][0][0])
            if d[0][0]["peak"].size > 0:
                f_mnt_res_peak.append(d[0][0]["peak"][0])
            else:
                f_mnt_res_peak.append(None)
        f_mnt_res_info = {
            "res_val": f_mnt_res_val,
            "res_fit": f_mnt_res_fit,
            "expt_type": f_mnt_res_type,
            "rxn_id": f_mnt_res_id,
            "res_stdev": f_mnt_res_std,
            "time_point": f_mnt_res_time,
            "experiment_id": f_mnt_res_expt,
            "res_data": f_mnt_res_data,
            "res_peak": f_mnt_res_peak,
        }
        return f_mnt_res_info

    def sort_residual_info(self, f_mnt_res_info, simulation_info, fittedData):
        """
        Seperate the information from the original input, the
        "get_residuals_info(f)" function, the "extract_file_info(filename)"
        function and the "extract_base_stats(f, simulation_id, info)" function
        into appropriate rows

        Parameters
        ----------
        f_mnt_res_info: dict
            the output of the "get_residuals_info(f)" function
        simulation_info: pandas.DataFrame
            the MS fragment file corresponding to
            the simulation
        fittedData: pandas.DataFrame
            the output of the
            "extract_base_stats(f, simulation_id, info)" function

        Returns
        -------
        fittedMeasuredFluxResiduals: pandas.DataFrame
            info about the residuals of the
            fluxes used as an input for the simulation
        fittedMeasuredFragmentResiduals: pandas.DataFrame
            info about the residuals of
            the fragments in the MS data used as an input for
            the simulation
        """

        fittedMeasuredFluxResiduals = {}
        fittedMeasuredFragmentResiduals = {}

        expt_type = f_mnt_res_info["expt_type"]
        experiment_id = f_mnt_res_info["experiment_id"]
        time_point = f_mnt_res_info["time_point"]
        rxn_id = f_mnt_res_info["rxn_id"]
        res_data = f_mnt_res_info["res_data"]
        res_fit = f_mnt_res_info["res_fit"]
        res_peak = f_mnt_res_info["res_peak"]
        res_stdev = f_mnt_res_info["res_stdev"]
        res_val = f_mnt_res_info["res_val"]
        simulation_id = fittedData["simulation_id"].unique()[0]
        simulation_dateAndTime = fittedData["simulation_dateAndTime"].unique()[
            0
        ]

        for cnt, x_type in enumerate(expt_type):
            if x_type == "Flux":
                if experiment_id[cnt] in list(
                    simulation_info["experiment_id"]
                ):
                    fittedMeasuredFluxResiduals[cnt] = {
                        "simulation_id": simulation_id,
                        "simulation_dateAndTime": simulation_dateAndTime,
                        "experiment_id": experiment_id[cnt],
                        "sample_name_abbreviation": simulation_info[
                            "sample_name_abbreviation"
                        ][0],
                        "time_point": time_point[cnt],
                        "rxn_id": rxn_id[cnt],
                        "res_data": float(res_data[cnt]),
                        "res_fit": float(res_fit[cnt]),
                        "res_peak": res_peak[cnt],
                        "res_stdev": float(res_stdev[cnt]),
                        "res_val": float(res_val[cnt]),
                        "res_msens": None,
                        "res_esens": None,
                        "used_": True,
                        "comment_": None,
                    }
                elif experiment_id[cnt] in list(
                    simulation_info["sample_name_abbreviation"]
                ):
                    fittedMeasuredFluxResiduals[cnt] = {
                        "simulation_id": simulation_id,
                        "simulation_dateAndTime": simulation_dateAndTime,
                        "experiment_id": simulation_info["experiment_id"][0],
                        "sample_name_abbreviation": experiment_id[cnt],
                        "time_point": time_point[cnt],
                        "rxn_id": rxn_id[cnt],
                        "res_data": float(res_data[cnt]),
                        "res_fit": float(res_fit[cnt]),
                        "res_peak": res_peak[cnt],
                        "res_stdev": float(res_stdev[cnt]),
                        "res_val": float(res_val[cnt]),
                        "res_msens": None,
                        "res_esens": None,
                        "used_": True,
                        "comment_": None,
                    }
            elif x_type == "MS":
                # parse the id into fragment_id and mass
                fragment_string = rxn_id[cnt]
                fragment_string = re.sub("_DASH_", "-", fragment_string)
                fragment_string = re.sub(
                    "_LPARANTHES_", "[(]", fragment_string
                )
                fragment_string = re.sub(
                    "_RPARANTHES_", "[)]", fragment_string
                )
                fragment_list = fragment_string.split("_")
                if not len(fragment_list) > 5 or not (
                    "MRM" in fragment_list or "EPI" in fragment_list
                ):
                    fragment_id = "_".join(
                        [fragment_list[0], fragment_list[1], fragment_list[2]]
                    )
                    fragment_mass = Formula(fragment_list[2]).mass + float(
                        fragment_list[3]
                    )
                    time_point = fragment_list[4]
                else:
                    fragment_id = "_".join(
                        [
                            fragment_list[0],
                            fragment_list[1],
                            fragment_list[2],
                            fragment_list[3],
                        ]
                    )
                    fragment_mass = Formula(fragment_list[2]).mass + float(
                        fragment_list[4]
                    )
                    time_point = fragment_list[5]
                fragment_id = re.sub("-", "_DASH_", fragment_id)
                fragment_id = re.sub("[(]", "_LPARANTHES_", fragment_id)
                fragment_id = re.sub("[)]", "_RPARANTHES_", fragment_id)
                if experiment_id[cnt] in list(
                    simulation_info["experiment_id"]
                ):
                    fittedMeasuredFragmentResiduals[cnt] = {
                        "simulation_id": simulation_id,
                        "simulation_dateAndTime": simulation_dateAndTime,
                        "experiment_id": experiment_id[cnt],
                        "sample_name_abbreviation": simulation_info[
                            "sample_name_abbreviation"
                        ][0],
                        "time_point": time_point,
                        "fragment_id": fragment_id,
                        "fragment_mass": fragment_mass,
                        "res_data": float(res_data[cnt]),
                        "res_fit": float(res_fit[cnt]),
                        "res_peak": res_peak[cnt],
                        "res_stdev": float(res_stdev[cnt]),
                        "res_val": float(res_val[cnt]),
                        "res_msens": None,
                        "res_esens": None,
                        "used_": True,
                        "comment_": None,
                    }
                elif experiment_id[cnt] in list(
                    simulation_info["sample_name_abbreviation"]
                ):
                    fittedMeasuredFragmentResiduals[cnt] = {
                        "simulation_id": simulation_id,
                        "simulation_dateAndTime": simulation_dateAndTime,
                        "experiment_id": simulation_info["experiment_id"][0],
                        "sample_name_abbreviation": experiment_id[cnt],
                        "time_point": time_point[cnt],
                        "fragment_id": fragment_id,
                        "fragment_mass": fragment_mass,
                        "res_data": float(res_data[cnt]),
                        "res_fit": float(res_fit[cnt]),
                        "res_peak": res_peak[cnt],
                        "res_stdev": float(res_stdev[cnt]),
                        "res_val": float(res_val[cnt]),
                        "res_msens": None,
                        "res_esens": None,
                        "used_": True,
                        "comment_": None,
                    }
            else:
                print("type not recognized")
        fittedMeasuredFluxResiduals = pd.DataFrame.from_dict(
            fittedMeasuredFluxResiduals, "index"
        )
        fittedMeasuredFragmentResiduals = pd.DataFrame.from_dict(
            fittedMeasuredFragmentResiduals, "index"
        )
        return fittedMeasuredFluxResiduals, fittedMeasuredFragmentResiduals

    def get_fitted_parameters(self, f, simulation_info):
        """
        Extract the fitted parameters

        Parameters
        ----------
        f: scipy.MatlabObject
            the fit of the model
        simulation_info: pandas.DataFrame
            the MS fragment file corresponding to
            the simulation

        Returns
        -------
        f_par_info: dict
            a dict containing the reaction id,
            the corresponding flux value, the fluxes standard deviation,
            the type of the flux (net flux or norm), the lower and upper
            bounds of the flux,
            the fluxes unit, the alf, the chi2 values of the fit,
            a correlation parameter,
            the fluxes covariance and a boolean describing if it's a free
            flux or not.
        """
        f_par_id = []
        f_par_val = []
        f_par_std = []
        f_par_type = []  # 'Net flux' or 'Norm'
        f_par_lb = []
        f_par_ub = []
        f_par_unit = []
        f_par_alf = []
        f_par_chi2s = []
        f_par_cor = []
        f_par_cov = []
        f_par_free = []
        for d in f["par"][0][0][0]["id"]:
            if "Expt #1" in d[0]:
                id_str = d[0].astype("str")
                f_par_id.append(
                    id_str.replace(
                        "Expt #1", simulation_info["experiment_id"][0]
                    )
                )
            else:
                f_par_id.append(d[0])
        # ensure that there are no negative values or infinite values
        for d in f["par"][0][0][0]["val"]:
            if not d:
                f_par_val.append(0.0)
            elif isnan(d[0][0]):
                f_par_val.append(0.0)
            elif isinf(d[0][0]):
                f_par_val.append(1.0e3)
            else:
                f_par_val.append(float(d[0][0]))
        for d in f["par"][0][0][0]["std"]:
            if not d:
                f_par_std.append(0.0)
            elif isnan(d[0][0]):
                f_par_val.append(0.0)
            else:
                f_par_std.append(float(d[0][0]))
        for d in f["par"][0][0][0]["type"]:
            f_par_type.append(d[0])
        # adjust the lb and ub to [0,1000];
        for cnt, d in enumerate(f["par"][0][0][0]["lb"]):
            if d.size == 0:
                f_par_lb.append(0.0)
            elif isnan(d[0][0]):
                f_par_lb.append(0.0)
            else:
                f_par_lb.append(float(d[0][0]))
        for d in f["par"][0][0][0]["ub"]:
            if d.size == 0:
                f_par_ub.append(1.0e3)
            elif isinf(d[0][0]) or isnan(d[0][0]):
                f_par_ub.append(1.0e3)
            else:
                f_par_ub.append(float(d[0][0]))
        for d in f["par"][0][0][0]["unit"]:
            if d.size == 0:
                f_par_unit.append("mmol*gDCW-1*hr-1")
            else:
                f_par_unit.append(d[0])
        for d in f["par"][0][0][0]["alf"]:
            f_par_alf.append(float(d[0][0]))
        for d in f["par"][0][0][0]["chi2s"]:
            f_par_chi2s.append(d)
        for d in f["par"][0][0][0]["cor"]:
            f_par_cor.append(d)
        for d in f["par"][0][0][0]["cov"]:
            f_par_cov.append(d)
        for d in f["par"][0][0][0]["free"]:
            f_par_free.append(bool(d[0][0]))
        f_par_info = {
            "rxn_id": f_par_id,
            "flux": f_par_val,
            "flux_stdev": f_par_std,
            "par_type": f_par_type,
            "flux_lb": f_par_lb,
            "flux_ub": f_par_ub,
            "flux_units": f_par_unit,
            "fit_alf": f_par_alf,
            "fit_chi2s": f_par_chi2s,
            "fit_cor": f_par_cor,
            "fit_cov": f_par_cov,
            "free": f_par_free,
        }
        return f_par_info

    # fit_cor, f_par_cov and fit_chi2s produce quite a lot of output,
    # they are arrays, so they were set to "None". If desired, set them to
    # f_par_c**[cnt] (the variable names can be found right underneath
    # the docstring)
    def sort_parameter_info(self, f_par_info, simulation_info, fittedData):
        """
        Seperate the information from the original input, the
        "get_fitted_parameters(f, simulation_info)"
        function, the "extract_file_info(filename)" function and the
        "extract_base_stats(f, simulation_id, info)" function
        into appropriate rows

        Parameters
        ----------
        f_par_info: dict
            output of the
            get_fitted_parameters(f, simulation_info) function
        simulation_info: pandas.DataFrame
            the MS fragment file corresponding to
            the simulation
        fittedData: pandas.DataFrame
            the output of the
            "extract_base_stats(f, simulation_id, info)" function

        Returns
        -------
        fittedFluxes: pandas.DataFrame
            info about the parameters of the fluxes used
            as an input for the simulation
        fittedFragments: pandas.DataFrame
            info about the parameters of the MS data
            used as an input for the simulation
        """
        fittedFluxes = {}
        fittedFragments = {}

        rxn_id = f_par_info["rxn_id"]
        flux = f_par_info["flux"]
        flux_stdev = f_par_info["flux_stdev"]
        par_type = f_par_info["par_type"]
        flux_lb = f_par_info["flux_lb"]
        flux_ub = f_par_info["flux_ub"]
        flux_units = f_par_info["flux_units"]
        fit_alf = f_par_info["fit_alf"]
        free = f_par_info["free"]
        # f_par_chi2s = f_par_info["fit_chi2s"]
        # f_par_cor = f_par_info["fit_cor"]
        # f_par_cov = f_par_info["fit_cov"]

        simulation_id = fittedData["simulation_id"].unique()[0]
        simulation_dateAndTime = fittedData["simulation_dateAndTime"].unique()[
            0
        ]

        for cnt, p_type in enumerate(par_type):
            if p_type == "Net flux":
                fittedFluxes[cnt] = {
                    "simulation_id": simulation_id,
                    "simulation_dateAndTime": simulation_dateAndTime,
                    "rxn_id": rxn_id[cnt],
                    "flux": flux[cnt],
                    "flux_stdev": flux_stdev[cnt],
                    "flux_lb": flux_lb[cnt],
                    "flux_ub": flux_ub[cnt],
                    "flux_units": flux_units[cnt],
                    "fit_alf": fit_alf[cnt],
                    "fit_chi2s": None,
                    "fit_cor": None,
                    "fit_cov": None,
                    "free": free[cnt],
                    "used_": True,
                    "comment_": None,
                }
            elif p_type == "Norm":
                # parse the id
                id_list = rxn_id[cnt].split(" ")
                expt = id_list[0]
                fragment_id = id_list[1]
                fragment_string = id_list[2]
                units = id_list[3]
                # parse the id into fragment_id and mass
                fragment_string = re.sub("_DASH_", "-", fragment_string)
                fragment_string = re.sub(
                    "_LPARANTHES_", "[(]", fragment_string
                )
                fragment_string = re.sub(
                    "_RPARANTHES_", "[)]", fragment_string
                )
                fragment_list = fragment_string.split("_")
                if not len(fragment_list) > 5 or not (
                    "MRM" in fragment_list or "EPI" in fragment_list
                ):
                    fragment_mass = Formula(fragment_list[2]).mass + float(
                        fragment_list[3]
                    )
                    time_point = fragment_list[4]
                else:
                    fragment_mass = Formula(fragment_list[2]).mass + float(
                        fragment_list[4]
                    )
                    time_point = fragment_list[5]
                if expt in list(simulation_info["experiment_id"]):
                    fittedFragments[cnt] = {
                        "simulation_id": simulation_id,
                        "simulation_dateAndTime": simulation_dateAndTime,
                        "experiment_id": expt,
                        "sample_name_abbreviation": simulation_info[
                            "sample_name_abbreviation"
                        ][0],
                        "time_point": time_point,
                        "fragment_id": fragment_id,
                        "fragment_mass": fragment_mass,
                        "fit_val": flux[cnt],
                        "fit_stdev": flux_stdev[cnt],
                        "fit_units": units,
                        "fit_alf": fit_alf[cnt],
                        "fit_cor": None,
                        "fit_cov": None,
                        "free": free[cnt],
                        "used_": True,
                        "comment_": None,
                    }
                elif expt in list(simulation_info["sample_name_abbreviation"]):
                    fittedFragments[cnt] = {
                        "simulation_id": simulation_id,
                        "simulation_dateAndTime": simulation_dateAndTime,
                        "experiment_id": simulation_info["experiment_id"][0],
                        "sample_name_abbreviation": expt,
                        "time_point": time_point,
                        "fragment_id": fragment_id,
                        "fragment_mass": fragment_mass,
                        "fit_val": flux[cnt],
                        "fit_stdev": flux_stdev[cnt],
                        "fit_units": units,
                        "fit_alf": fit_alf[cnt],
                        "fit_cor": None,
                        "fit_cov": None,
                        "free": free[cnt],
                        "used_": True,
                        "comment_": None,
                    }
            else:
                print("type not recognized")
        fittedFluxes = pd.DataFrame.from_dict(fittedFluxes, "index")
        fittedFragments = pd.DataFrame.from_dict(fittedFragments, "index")
        return fittedFluxes, fittedFragments

    def reimport(self, filename, simulation_info, simulation_id):
        """
        Summary function that includes all of the previously set up functions
        and produces all of the outputs

        Parameters
        ----------
        filename: str
            name of the .mat file we want to get information about
        simulation_info: pandas.DataFrame
            The MS fragment file corresponding to the simulation
        simulation_id: str
            The name of the experiment used for the simulation as in the MS
            fragment file

        Returns
        -------
        fittedData: pandas.DataFrame
            base statistics describing the fit
        fittedFluxes: pandas.DataFrame
            info about the fitted fluxes
        fittedFragments: pandas.DataFrame
            info about the fitted fragments
        fittedMeasuredFluxes: pandas.DataFrame
            info about the fluxes used as an input for the simulation
        fittedMeasuredFragments: pandas.DataFrame
            info about the MS data used as an input for the simulation
        fittedMeasuredFluxResiduals: pandas.DataFrame
            info about the residuals of the fluxes used as an input for
            the simulation
        fittedMeasuredFragmentResiduals: pandas.DataFrame
            info about the residuals of the fragments in the
            MS data used as an input for the simulation
        simulationParameters: pandas.DataFrame
            the simulation parameters
        """
        # Succession of functions
        info = self.extract_file_info(filename)
        parallel, non_stationary = self.det_simulation_type(simulation_info)
        m, f = self.data_extraction(filename)
        # model_info = self.extract_model_info(m)
        # not used for the final output
        simulationParameters = self.extract_sim_params(
            simulation_id, info, m, filename
        )
        fittedData = self.extract_base_stats(f, simulation_id, info)
        f_mnt_info = self.get_fit_info(f)
        fittedMeasuredFluxes, fittedMeasuredFragments = self.sort_fit_info(
            f_mnt_info, simulation_info, fittedData
        )
        f_mnt_res_info = self.get_residuals_info(f, simulation_info)
        (
            fittedMeasuredFluxResiduals,
            fittedMeasuredFragmentResiduals,
        ) = self.sort_residual_info(
            f_mnt_res_info, simulation_info, fittedData
        )
        f_par_info = self.get_fitted_parameters(f, simulation_info)
        fittedFluxes, fittedFragments = self.sort_parameter_info(
            f_par_info, simulation_info, fittedData
        )
        return (
            fittedData,
            fittedFluxes,
            fittedFragments,
            fittedMeasuredFluxes,
            fittedMeasuredFragments,
            fittedMeasuredFluxResiduals,
            fittedMeasuredFragmentResiduals,
            simulationParameters,
        )
