# Module used to build SQL statements to interact with the reaction rules database

__all__ = []

import json

import numpy as np
from pypika import Case, Criterion, Tables, Query
from pypika.terms import AggregateFunction

from BFAIR.pathways.utils import calculate_similarity

rules, reactions, metabolites, classification, stoichiometry, thesaurus = Tables(
    "rules", "reactions", "metabolites", "classification", "stoichiometry", "thesaurus"
)


class ChemicalSimilarity:
    """Function to aggregate inputs by chemical similarity. To be used in SQL statements."""

    @classmethod
    def Function(cls, a, b):
        return AggregateFunction(cls.__name__, a, b)

    def __init__(self):
        self.scores = []

    def step(self, a, b):
        self.scores.append(calculate_similarity(json.loads(a), json.loads(b)))

    def finalize(self):
        if self.scores:
            return np.max(self.scores)


def select_rules_where(filters) -> str:
    """
    Returns a SQL statement that (based on a series of filters) selects reaction rules, their associated MetaNetX ID,
    and SMARTS expression.

    Parameters
    ----------
    filters : list of pypika.terms.Criterion
        Criteria that the rules should satisfy. Feeds the WHERE statement.

    Returns
    -------
    str
        SQL SELECT statement.
    """
    return (
        Query.from_(rules)
        .select(rules.rule_id, rules.reaction_id, rules.smarts)
        .where(Criterion.all(filters))
        .get_sql()
    )


def select_rules_by_reaction_id(reaction_ids, filters=None) -> str:
    """
    Returns a SQL statement that selects reaction rules based on their associated MetaNetX ID.

    Parameters
    ----------
    reaction_ids : list
        List of MetaNetX reaction identifiers.
    filters : list of pypika.terms.Criterion
        Criteria that the rules should also satisfy. Feeds the WHERE statement.

    Returns
    -------
    str
        SQL SELECT statement.
    """
    if filters is None:
        filters = []
    # Join 'rules' to 'thesaurus' on 'thesaurus.synonym' to account for internal synonymous IDs
    # Select rules by 'rules.reaction_id' or 'thesaurus.id'
    return (
        Query.from_(rules)
        .left_join(thesaurus)
        .on(rules.reaction_id == thesaurus.synonym)
        .select(rules.rule_id)
        .where(Criterion.all([rules.reaction_id.isin(reaction_ids) | thesaurus.id.isin(reaction_ids), *filters]))
        .get_sql()
    )


def select_rules_by_synonymous_id(reaction_ids, filters=None) -> str:
    """
    Returns a SQL statement that selects reaction rules based on a synonym of their associated MetaNetX ID.

    Parameters
    ----------
    reaction_ids : list
        List of MetaNetX reaction identifiers.
    filters : list of pypika.terms.Criterion
        Criteria that the rules should also satisfy. Feeds the WHERE statement.

    Returns
    -------
    str
        SQL SELECT statement.
    """
    if filters is None:
        filters = []
    # Join 'rules' to 'thesaurus' on 'thesaurus.id' to account for external (i.e., user-input) synonymous IDs
    # Select rules by 'thesaurus.synonym'
    return (
        Query.from_(rules)
        .left_join(thesaurus)
        .on(rules.reaction_id == thesaurus.id)
        .select(rules.rule_id)
        .where(Criterion.all([thesaurus.synonym.isin(reaction_ids), *filters]))
        .get_sql()
    )


def select_rules_by_ec_number(ec_numbers, filters=None) -> str:
    """
    Returns a SQL statement that selects reaction rules based on their associated E.C. numbers.

    Parameters
    ----------
    ec_numbers : list
        List of E.C. numbers.
    filters : list of pypika.terms.Criterion
        Criteria that the rules should also satisfy. Feeds the WHERE statement.

    Returns
    -------
    str
        SQL SELECT statement.
    """
    if filters is None:
        filters = []
    return (
        Query.from_(rules)
        .left_join(classification)
        .on(rules.reaction_id == classification.reaction_id)
        .select(rules.rule_id)
        .where(Criterion.all([classification.ec_number.isin(ec_numbers), *filters]))
        .get_sql()
    )


def select_rules_by_similarity(input_fingerprint, cutoff, filters=None) -> str:
    """
    Returns a SQL statement that selects reaction rules whose substrates have a minimum chemical similarity with the
    input.

    Parameters
    ----------
    input_fingerprint : str
        Serialized molecular fingerprint of a chemical compound, against which substrates are compared.
    cutoff : float
        Chemical similarity score (between the input fingerprint and the fingerprint of a reaction's native substrate)
        below which rules are filtered out.
    filters : list of pypika.terms.Criterion
        Criteria that the rules should also satisfy. Feeds the WHERE statement.

    Returns
    -------
    str
        SQL SELECT statement.
    """
    if filters is None:
        filters = []
    return (
        Query.from_(rules)
        .join(stoichiometry)
        .on(rules.reaction_id == stoichiometry.reaction_id)
        .join(metabolites)
        .on(stoichiometry.substrate_id == metabolites.metabolite_id)
        .groupby(rules.rule_id)
        .having(ChemicalSimilarity.Function(input_fingerprint, metabolites.fingerprint) >= cutoff)
        .select(rules.rule_id)
        .where(Criterion.all(filters))
        .get_sql()
    )


def select_metabolites_by_inchi(inchi, filters=None):
    """
    Returns a SQL statement that selects metabolites based on their InChI depiction.

    Parameters
    ----------
    inchi : str
        InChI depiction of a chemical compound.
    filters : list of pypika.terms.Criterion
        Criteria that the metabolites should also satisfy. Feeds the WHERE statement.

    Returns
    -------
    str
        SQL SELECT statement.
    """
    if filters is None:
        filters = []
    # Join 'metabolites' to 'thesaurus' on 'thesaurus.synonym' to account for internal synonymous IDs
    # Select 'thesaurus.id' if exists, otherwise 'metabolites.metabolite_id' (meaning no synonym was found)
    return (
        Query.from_(metabolites)
        .left_join(thesaurus)
        .on(metabolites.metabolite_id == thesaurus.synonym)
        .select(Case().when(thesaurus.id.notnull(), thesaurus.id).else_(metabolites.metabolite_id).as_("metabolite_id"))
        .distinct()
        .where(Criterion.all([metabolites.inchi == inchi, *filters]))
        .get_sql()
    )
