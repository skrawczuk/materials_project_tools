import numpy as np
import pandas as pd
import pymatgen as mg
from pymatgen import MPRester


def query_database(criteria, api_key):
    properties = ['energy', 'energy_per_atom', 'volume', 'formation_energy_per_atom', 'nsites', 'unit_cell_formula',
                  'pretty_formula', 'is_hubbard', 'elements', 'nelements', 'e_above_hull', 'hubbards', 'is_compatible',
                  'spacegroup', 'task_ids', 'band_gap', 'density', 'icsd_id', 'icsd_ids', 'cif', 'total_magnetization',
                  'material_id', 'oxide_type', 'tags', 'elasticity']

    mprest = MPRester(api_key)
    results = mprest.query(criteria=criteria, properties=properties)
    results_df = pd.DataFrame(results)
    return results_df


def filter_n_most_stable(results_df, n):
    """
    remove materials that aren't among n most stable for formula within results_df
    """
    if n != -1:
        n_stable_results_df = pd.DataFrame()
        for _, material in results_df.groupby('pretty_formula'):
            sorted_material = material.sort_values(by='e_above_hull')
            material = sorted_material[:n]
            n_stable_results_df = n_stable_results_df.append(material)
        results_df = n_stable_results_df
    return results_df


def tmo_materials(n_most_stable: int, rows: list, n_elements: int, api_key: str):
    """
    Returns a dataframe of transition metal oxides
    Parameters
    ----------
    n_most_stable : int
        Of the formations of this material, the n with the lowest e_above_hull. -1 returns all
    rows: list[int]
        which rows of transition metals to include (4 - 7)
    n_elements : int
        number of UNIQUE elements to be in each compound. (3 would mean 2 TMs and O)
        NOT the total number of atoms
    api_key : str
        materials project API key. Find yours at: https://materialsproject.org/dashboard

    Returns
    -------
    results_df : data frame
        dataframe containing resulting entries from the database

    """

    all_elements = [i for i in mg.periodic_table.Element]
    trans_metals = [i for i in all_elements if np.any([i.row == r for r in rows]) and i.block == 'd']
    not_trans_metals = np.setdiff1d(all_elements, trans_metals)
    trans_metals = [i.symbol for i in trans_metals]
    not_trans_metals = [i.symbol for i in not_trans_metals if i.symbol != 'O']

    criteria = {'elements': {
        '$in': trans_metals,
        '$nin': not_trans_metals,
        '$all': ['O']},
        'nelements': {
            '$lte': n_elements}
    }

    results_df = query_database(criteria, api_key)
    results_df = filter_n_most_stable(results_df, n_most_stable)

    return results_df

