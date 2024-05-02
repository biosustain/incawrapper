"""This script creates a simulated data set for the C. necator model from (Alagesan, S., Minton, 
N.P. & Malys, N. 13C-assisted metabolic flux analysis to investigate heterotrophic and mixotrophic 
metabolism in Cupriavidus necator H16. Metabolomics 14, 9 (2018). 
https://doi.org/10.1007/s11306-017-1302-z). The data set is used to validate the INCAWrapper for 
medium size models. 

The simulation mimicks a two parallel experiments where C. necator is grown with labelled frucotse and 
labelled glycerol. We simulated MS measurements of the amino acids and a few 
exchanges fluxes are measured. To increase the information about the systems we simulate measurements 
of CO2 exchange flux. To do this we added one additional reaction to the original model, i.e. 
CO2 -> CO2.ext. The script will create a simulated data set and save it to the
simulated_data folder. The script also saves the model specification tables for later use.

The INCAWrapper does not include a good API for simulation, thus this is sometimes a bit hacky 
and requires some knowledge of how to use INCA Matlab scripts."""

# %%
import pandas as pd
import numpy as np
import pathlib
import incawrapper
from incawrapper import run_inca
import ast

# %%
data_folder = pathlib.Path(__file__).parent
output_folder = data_folder / "simulated_data"
xl_file = pd.ExcelFile(data_folder / "MDV_raw.xlsx")
fragments = pd.read_csv(
    data_folder / "fragments.csv",
    sep="\t",
    converters={"labelled_atoms": ast.literal_eval},
)
USE_EXPERIMENT = [
    "simulation1",
    "simulation2",
    "simulation3",
    "simulation4",
    "simulation5",
    "simulation6",
    "simulation7",
    "simulation8",
    "simulation9",
]


# %% Read and process reaction data
reacts = pd.read_excel(data_folder / "reactions.xlsx")
reacts_renamed = reacts.copy().rename(
    columns={"Reaction ID": "rxn_id", "Equations (Carbon atom transition)": "rxn_eqn"}
)
reacts_merged = incawrapper.utils.merge_reaverible_reaction(reacts_renamed)
# Add CO2 exchange reaction
co2_exchange_reaction = pd.DataFrame(
    {
        "rxn_id": ["ex_3"],
        "rxn_eqn": ["CO2 -> CO2.ext"],
    }
)
reacts_added_co2_exchange = pd.concat([reacts_merged, co2_exchange_reaction])
reacts_processed = reacts_added_co2_exchange.copy()

# %% Setup tracer data
# We will setup the tracer data as done in the tutorial. However we will only
# simulate the fructose experiment.
tracer_info = pd.DataFrame.from_dict(
    {
        "experiment_id": [
            "simulation1",
            "simulation2",
            "simulation3",
            "simulation4",
            "simulation5",
            "simulation6",
            "simulation7",
            "simulation8",
            "simulation9",
        ],
        "met_id": ["FRU.ext"] * 6 + ["GLY.ext"] * 3,
        "tracer_id": [
            "D-[1-13C]fructose",
            "D-[2-13C]fructose",
            "D-[3-13C]fructose",
            "D-[4-13C]fructose",
            "D-[5-13C]fructose",
            "D-[6-13C]fructose",
            "[1-13C]-Glycerol",
            "[2-13C]-Glycerol",
            "[3-13C]-Glycerol",
        ],
        "atom_ids": [
            [1],
            [2],
            [3],
            [4],
            [5],
            [6],
            [1],
            [2],
            [3],
        ],
        "atom_mdv": [
            [0.0, 1.0],
            [0.0, 1.0],
            [0.0, 1.0],
            [0.0, 1.0],
            [0.0, 1.0],
            [0.0, 1.0],
            [0.0, 1.0],
            [0.0, 1.0],
            [0.0, 1.0],
        ],
        "enrichment": [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
        ],
    },
    orient="columns",
)

# %%
# INCA only save the simulation for the MDV that are measured.
# Thus, we will create some dummy measurements for the MDVs that
# we with to simulate. In our case easiest way to do this is to
# create the ms_data table as done in the tutorial and then
# remove the measurements.

# Code from the tutorial
def parse_mdv_raw_to_long(df: pd.DataFrame, experiment_id: str) -> pd.DataFrame:
    df["Amino Acid"] = df["Amino Acid"].ffill()
    long = df.melt(
        id_vars=["Amino Acid", "Unnamed: 1", "m/z"], var_name="mass_isotope"
    ).drop(columns=["Unnamed: 1"])
    long[["intensity", "intensity_std_error"]] = long["value"].str.split(
        r"±|\+", regex=True, expand=True
    )
    long.drop(columns=["value"], inplace=True)

    # convert strings to floats
    long["intensity"] = long["intensity"].str.strip().astype(float)
    long["intensity_std_error"] = long["intensity_std_error"].str.strip().astype(float)

    # some amino acids have trailing spaces
    long["Amino Acid"] = long["Amino Acid"].str.strip()

    # make ids
    long["fragment_id"] = long["Amino Acid"].str.replace(" ", "") + long["m/z"].astype(
        str
    )
    long["experiment_id"] = experiment_id
    return long.dropna()


mdvs_long = pd.DataFrame()
mdvs_raw = xl_file.parse("fructose")
mdvs_long = parse_mdv_raw_to_long(mdvs_raw, experiment_id="fructose")
mdvs_long.reset_index(drop=True, inplace=True)


met_abbriviations = {
    "Alanine": "ALA",
    "Aspartic acid": "ASP",
    "Glycine": "GL",
    "Glutamic acid": "GLU",
    "Histidine": "HIS",
    "Isoleucine": "ILE",
    "Leucine": "LEU",
    "Methionine": "MET",
    "Phenylalanine": "PHE",
    "Serine": "SER",
    "Threonine": "THR",
    "Valine": "VAL",
}
mdvs_long["met_id"] = mdvs_long["Amino Acid"].map(met_abbriviations)


def mass_isotope_to_int(mass_isotope: str) -> int:
    if isinstance(mass_isotope, int):  # avoids error when rerunning the cell
        return mass_isotope
    elif mass_isotope == "M":
        return 0
    else:
        return int(mass_isotope.replace("M+", ""))


mdvs_long["mass_isotope"] = mdvs_long["mass_isotope"].apply(mass_isotope_to_int)
ms_data_one_exp = (
    mdvs_long.merge(
        fragments[["fragment_id", "labelled_atoms", "unlabelled_atoms"]],
        on="fragment_id",
        how="left",
    )
    .rename(
        columns={  # rename columns to match the schema
            "fragment_id": "ms_id",
            "labelled_atoms": "labelled_atom_ids",
        }
    )
    .drop(columns=["Amino Acid", "m/z"])
)

ms_data_one_exp["time"] = np.inf
ms_data_one_exp["measurement_replicate"] = 1
ms_data_one_exp = ms_data_one_exp.query('ms_id != "Methionine292"')

# replace measured values with NaN
ms_data_one_exp["intensity"] = np.nan
ms_data_one_exp["intensity_std_error"] = np.nan

# Create a set of measurement per experiment
ms_data = pd.DataFrame()
for experiment_id in USE_EXPERIMENT:
    ms_data_one_exp["experiment_id"] = experiment_id
    ms_data = pd.concat([ms_data, ms_data_one_exp])

# %% Setup the INCA simulation script
output_file = pathlib.Path(data_folder / "c_necator_simulation.mat")
script = incawrapper.create_inca_script_from_data(
    reactions_data=reacts_processed,
    tracer_data=tracer_info,
    ms_measurements=ms_data,
    experiment_ids=USE_EXPERIMENT,
)
script.add_to_block(
    "options", incawrapper.define_options(sim_more=True, sim_na=True, sim_ss=True)
)
script.add_to_block(
    "runner",
    incawrapper.define_runner(output_file, run_estimate=False, run_simulation=True),
)

# In the following we set the flux distribution that we wish to simulate.
# To avoid having to specify a feasible flux distribution we will guess
# a flux distribution, fix the input flux value and then find the nearest
# feasible flux distribution.

# find number of reactions in the model
n_reactions = reacts_processed.shape[0]
n_reverse_reactions = reacts_processed["rxn_eqn"].str.contains("<->").sum()
total_fluxes = n_reactions + n_reverse_reactions

# Guess that all fluxes are 100
fluxes = np.array([100] * total_fluxes)
# %%

# This section of the INCA script defines the flux distribution that we wish to simulate.
script.add_to_block(
    block_name="model_modifications",
    matlab_script_block="""
m.rates.flx.val = ["""
    + " ".join(fluxes.astype(str))
    + """];
m.rates(1).flx.fix = true; % fix the value so it does not change when finding the nearest feasible flux distribution
"""
    + """% Find nearest feasible flux solution
m.rates.flx.val = transpose(mod2stoich(m));
""",
)
# %%
# Now we can run the INCA script
import dotenv

inca_directory = pathlib.Path(
    dotenv.get_key(dotenv.find_dotenv(), "INCA_base_directory")
)
incawrapper.run_inca(script, INCA_base_directory=inca_directory)

# %% Process the simulated data
res = incawrapper.INCAResults(output_file)
simulated_data = res.simulation.simulated_data

# fetch the ground truth values
true_fluxes = res.model.rates_in_net_exch_format

# %% Add metadata to the simulated data
simulated_mdv = (
    pd.merge(
        ms_data,
        simulated_data,
        left_on=["experiment_id", "ms_id", "mass_isotope", "time"],
        right_on=["expt", "id", "mass_isotope", "time"],
    )
    .drop(columns=["expt", "id", "type", "intensity"])
    .rename(columns={"mdv": "intensity"})
    .assign(intensity_std_error=0.003)
)


# %% Flux measurement

# The exchange fluxes are measured to the same value in both parallel experiments
flux_measurements = pd.DataFrame()
for experiment_id in USE_EXPERIMENT:
    # fetch the flux measurements
    fluxes = true_fluxes.query("rxn_id in ['ex_1', 'ex_2', 'R72', 'ex_3']").copy()
    fluxes["experiment_id"] = experiment_id
    fluxes["flux_std_error"] = fluxes["flux"] * 0.003
    flux_measurements = pd.concat([flux_measurements, fluxes])
# %%

# save ground truth values and simulated data
simulated_mdv.to_csv(output_folder / "mdv_no_noise.csv", index=False)

flux_measurements.to_csv(output_folder / "flux_measurements_no_noise.csv", index=False)
true_fluxes.to_csv(output_folder / "true_fluxes.csv", index=False)


# save the processed model specification tables for later use
reacts_processed.to_csv(output_folder / "reactions_processed.csv", index=False)
tracer_info.to_csv(output_folder / "tracer_info.csv", index=False)

# %%
