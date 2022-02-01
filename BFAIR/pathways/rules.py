"""Rules.

This module contains functions to apply reaction rules to chemical compounds.
"""

__all__ = ["RuleLibrary"]

import json
import sqlite3 as sql
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from contextlib import AbstractContextManager
from itertools import chain
from typing import Generator

import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem

from BFAIR import models
from BFAIR.io.remote import LOCAL_PATH, fetch_remote
from BFAIR.logger import get_logger
from BFAIR.pathways.constants import CURRENCY_METABOLITES
from BFAIR.pathways.standardization import standardize
from BFAIR.pathways.utils import get_compound, get_molecular_fingerprint
from BFAIR.pathways import _queries as q


_ReactionResult = namedtuple("ReactionResult", ["rule_id", "reaction_id", "product_sets"])


class _RuleSimulator:
    # Simulates a reaction

    def __init__(self, compound: AllChem.Mol, reaction_smarts: str):
        self._compound = compound
        self._reaction = AllChem.ReactionFromSmarts(reaction_smarts)
        self._reaction.Initialize()
        self._interrupted = False

    def __call__(self):
        # can_run = any([compound.HasSubstructMatch(substrate) for substrate in reaction.GetReactants()])
        results = {}
        for products in self._reaction.RunReactants((self._compound,)):
            if self._interrupted:
                break
            products = [
                standardize(frag)
                for product in products
                for frag in Chem.GetMolFrags(product, asMols=True, sanitizeFrags=False)
            ]
            inchis = [Chem.MolToInchi(product) for product in products]
            results.setdefault(".".join(inchis), inchis)
        return [*results.values()]

    def interrupt(self):
        self._interrupted = True


class RuleLibrary(AbstractContextManager):
    """Rule Library.

    The Rule Library object connects to the reaction rules database and exposes functions to filter the reaction rules
    by different criteria.

    Parameters
    ----------
    pathname : Path, optional
        Pathname to the reaction rule database. If it does not exist, the database will be downloaded into it.
    **kwargs
        Standardization parameters applied to input compounds, see `BFAIR.pathways.utils.standardize`. Thorough
        standardization is enforced.

    Attributes
    ----------
    available : pandas.DataFrame
        A dataframe with the available rules (after filters applied). It has columns for rule ID, associated MetaNetX
        ID, and SMARTS expression.

    See Also
    --------
    utils.standardize
    """

    def __init__(self, pathname=None, **kwargs):
        self._logger = get_logger(__name__)
        kwargs.setdefault("add_hs", True)
        if not kwargs["add_hs"]:
            raise NotImplementedError()
        kwargs["remove_stereo"] = True
        if "thorough" in kwargs:
            self._logger.info("Thorough standardization will be enforced. Changing 'thorough' to True.")
        kwargs["thorough"] = True
        self._std_args = kwargs.copy()
        self._conn = None
        self._cursor = None
        self._filters = []
        self._pathname = self._download_database(pathname)
        self.open()

    def __iter__(self):
        return self.available.itertuples(index=False, name=None)

    def __len__(self):
        return len(self.available)

    def __repr__(self):
        return repr(self.available)

    def _repr_html_(self):
        return self.available._repr_html_()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    @property
    def available(self) -> pd.DataFrame:
        try:
            return pd.read_sql(q.select_rules_where(self._filters), self._conn, index_col="rule_id")
        except sql.ProgrammingError as exception:
            return pd.DataFrame([str(exception)], columns=["message"])

    def _download_database(self, pathname) -> str:
        # Download database if need be
        canonical_filename = f"rules_{'' if self._std_args['add_hs'] else 'no'}hs.db"
        if pathname is None:
            pathname = LOCAL_PATH / canonical_filename
        if not pathname.exists():
            self._logger.info(f"Database missing from `{pathname.parent}`. Downloading…")
            fetch_remote(canonical_filename, pathname)
        else:
            self._logger.debug("Database exists.")
        return pathname

    def _fetch_results(self, query) -> set:
        # Returns a set of unique results obtained by executing the specified SQL statement
        return set(chain.from_iterable(self._cursor.execute(query)))

    def open(self):
        """
        Connects to the SQL database.

        Returns
        -------
        same type as caller
        """
        self._conn = sql.connect(str(self._pathname))
        self._conn.create_aggregate(q.ChemicalSimilarity.__name__, 2, q.ChemicalSimilarity)
        self._cursor = self._conn.cursor()
        return self

    def close(self):
        """
        Closes the connection to the SQL database.

        Returns
        -------
        same type as caller
        """
        self._conn.close()
        return self

    def apply_to(self, input_compound, input_type="inchi", timeout=60.0) -> Generator:
        """
        Applies the available rules to the input compound.

        Parameters
        ----------
        input_compound : str or rdkit.Chem.rdchem.Mol
            String representation of a compound or a RDKit molecule object.
        input_type : {'inchi', 'smiles', 'rdkit'}
            Type of notation describing the input compound.
        timeout : float
            Number of seconds after which a rule simulation will be stopped.

        Yields
        ------
        tuple
            A tuple containing the applied rule ID, its associated MetaNetX ID, and a list of product sets. Note that a
            reaction may output more than one set of products.
        """
        available_rules = self.available
        compound = get_compound(input_compound, input_type, **self._std_args)
        with ThreadPoolExecutor(max_workers=1) as executor:
            tasks = (_RuleSimulator(compound, reaction_smarts) for reaction_smarts in available_rules["smarts"])
            for i, (task, future) in enumerate(((task, executor.submit(task)) for task in tasks)):
                try:
                    product_sets = future.result(timeout)
                    if not product_sets:
                        # Sometimes the reaction does not return any products
                        continue
                    yield _ReactionResult(
                        available_rules.index[i], available_rules.iloc[i]["reaction_id"], product_sets
                    )
                except TimeoutError:
                    self._logger.warn(f"Timed out processing rule '{available_rules.index[i]}'.")
                    task.interrupt()

    def list_products(self, input_compound, input_type="inchi", timeout=60.0) -> dict:
        """
        Applies available rules to input compound and processes reaction results into a dictionary containing an entry
        for each product and list of which reactions generated it.

        Parameters
        ----------
        input_compound : str or rdkit.Chem.rdchem.Mol
            String representation of a compound or a RDKit molecule object.
        input_type : {'inchi', 'smiles', 'rdkit'}
            Type of notation describing the input compound.
        timeout : float
            Number of seconds after which a rule simulation will be stopped.

        Returns
        -------
        dict
            A dictionary of (InChI depiction, list) pairs. InChI strings correspond to products resulting from input
            compound, whereas values are a list of 2-element tuples containing a reaction rule ID and MetaNetX ID
            indicating which reaction produced such product.

        Notes
        -----
        Currency metabolites (such as CoA and NADH) are omitted from the output.
        """
        results = {}
        for result in self.apply_to(input_compound, input_type, timeout):
            for products in result.product_sets:
                for inchi in products:
                    # Check if the InChi matches that of a currency metabolite
                    is_currency_metabolite_query = q.select_metabolites_by_inchi(
                        inchi, [q.metabolites.metabolite_id.isin(CURRENCY_METABOLITES)]
                    )
                    if self._fetch_results(is_currency_metabolite_query):
                        continue
                    results.setdefault(inchi, []).append((result.rule_id, result.reaction_id))
        return results

    def filter_by_diameter(self, cutoff):
        """
        Applies a filter to exclude rules that do not meet the diameter criteria.

        Parameters
        ----------
        cutoff : {2, 4, 6, 8, 10, 12, 14, 16}
            Diameter below which rules are filtered out. The diameter is a proxy for enzyme promiscuity. Formally, it is
            defined as the distance in molecular bonds around the reaction center. Thus, small diameters capture general
            reactions; whereas, bigg diameters correspond to specific reactions.

        Returns
        -------
        same type as caller

        Raises
        ------
        ValueError
            If an unsupported diameter type is specified.
        """
        if cutoff not in tuple(range(2, 18, 2)):
            raise ValueError(f"Unsupported diameter: {cutoff}. See allowed values in documentation.")
        self._filters.append(q.rules.diameter >= cutoff)
        return self

    def filter_by_organism(self, model_name=None, additional_identifiers=None, additional_ec_numbers=None):
        """
        Applies a filter to the rule library that excludes reactions that are not present in an input genome-scale
        model.

        Parameters
        ----------
        model_name : str
            The name of a genome-scale model, from which MetaNetX reaction identifiers will be extracted. Currently,
            only pre-curated models are supported. See `BFAIR.models` for a list of available models.
        additional_identifiers, additional_ec_numbers : list of str
            List of additional MetaNetX reaction identifiers or E.C. numbers that are considered as part of the
            organism. These can be, for instance, used to include heterologous enzymatic steps not described in the
            genome-scale model.

        Returns
        -------
        same type as caller
        """
        reaction_ids = set(additional_identifiers) if additional_identifiers is not None else set()
        ec_numbers = set(additional_ec_numbers) if additional_ec_numbers is not None else set()
        # TODO Accept custom models
        if model_name:
            model = getattr(models, model_name)
            for rxn in model.reactions:
                reaction_id = rxn.annotation.get("metanetx.reaction", None)
                if reaction_id:
                    reaction_ids.add(reaction_id)
                ec_num = rxn.annotation.get("ec-code", [])
                if isinstance(ec_num, str):
                    ec_numbers.add(ec_num)
                else:
                    ec_numbers.update(ec_num)

        fetched_rules = set()
        if reaction_ids:
            fetched_rules.update(self._fetch_results(q.select_rules_by_reaction_id(reaction_ids, self._filters)))
            # because internal or external reaction IDs can be deprecated, we should look for synonyms in the thesaurus
            fetched_rules.update(self._fetch_results(q.select_rules_by_synonymous_id(reaction_ids, self._filters)))

        if ec_numbers:
            fetched_rules.update(self._fetch_results(q.select_rules_by_ec_number(ec_numbers, self._filters)))

        if not fetched_rules:
            self._logger.error("The model has no identifiable reactions.")
        else:
            self._logger.debug(
                f"Filtered rules based on {len(reaction_ids)} MetaNetX IDs and {len(ec_numbers)} E.C. numbers."
            )

        self._filters.append(q.rules.rule_id.isin(fetched_rules))

        return self

    def filter_by_compound(self, input_compound, input_type="inchi", cutoff=0.7):
        """
        Applies a filter to exclude rules that cannot be applied to an input compound. Applicability is based on
        chemical similarity.

        Parameters
        ----------
        input_compound : str or rdkit.Chem.rdchem.Mol
            String representation of a compound or a RDKit molecule object.
        input_type : {'inchi', 'smiles', 'rdkit'}
            Type of notation describing the input compound.
        cutoff : float
            Chemical similarity score (between the input compound and the native substrate of a reaction) below which a
            reaction rule is considered inapplicable. The chemical similarity score between two compounds ranges from 0
            to 1, the latter meaning both molecules are identical.

        Returns
        -------
        same type as caller
        """
        input_fp = json.dumps(get_molecular_fingerprint(input_compound, input_type, **self._std_args))

        # Execute query and create new criterion for rules matching the resulting IDs
        # We use this new criterion instead of a sub-query to avoid overhead costs of fingerprint calculation
        fetched_rules = self._fetch_results(q.select_rules_by_similarity(input_fp, cutoff, self._filters))

        if not fetched_rules:
            self._logger.warn(f"No reaction rules match the given compound:\n{input_compound}")

        self._filters.append(q.rules.rule_id.isin(fetched_rules))

        return self

    def filter_by_uncertainty(self, cutoff=0.1):
        """
        Applies a filter to exclude rules that do not meet the biochemical uncertainty criteria.

        Parameters
        ----------
        cutoff : float
            Biochemical uncertainty score below which reaction rules are filtered out. Each reaction rule has an
            associated score that functions as a proxy for uncertainty and specificity. Scores closer to 1 indicate less
            uncertainty and higher specificity with respect to the annotated enzyme sequences.

        Returns
        -------
        same type as caller
        """
        self._filters.append(q.rules.score >= cutoff)
        return self

    def pop_filter(self, index=-1):
        """
        Removes a filter criterion from the rule library.

        Parameters
        ----------
        index : int, default -1
            Index of filter to pop (the default is -1, which points to the last filter applied).

        Returns
        -------
        same type as caller
        """
        self._filters.pop(index)
        return self

    def reset(self):
        """
        Resets all the applied filters.

        Returns
        -------
        same type as caller
        """
        self._filters = []
        return self
