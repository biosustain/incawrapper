# generate test_data
# Last date : 09.12.2020
# By : Matthias Mattanovich (matmat@biosustain.dtu.dk)
# This script is intended to generate sample data and save them into the
# test_data file. The saved objects will then be used to test the
# INCAScript_generator using unit testing.
import pickle
import pandas as pd
import pathlib
from incawrapper.mfa.INCA import parse_cobra_model


current_dir = str(pathlib.Path(__file__).parent.absolute())

pd.set_option("mode.chained_assignment", None)
# Use pickle to save python variables
filehandler = open("input_parser_test_data.obj", "wb")

coli_model = parse_cobra_model('Models/iJO1366.json', 'iJO1366', 'today')

celegans_model = parse_cobra_model('Models/wormjam-20180125.sbml',
                                   'wormjam-20180125', 'today')

pickle.dump(
    [
        coli_model,
        celegans_model,
    ],
    filehandler,
)

filehandler.close()
