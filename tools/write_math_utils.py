#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hwrt import filter_dataset


def get_formulas(cursor, dataset='all'):
    """Get a list of formulas.

    Parameters
    ----------
    cursor : a database cursor
    dataset : string
        Either 'all' or a path to a yaml symbol file.

    Returns
    -------
    list :
        A list of formulas
    """
    if dataset == 'all':
        sql = ("SELECT `id`, `formula_in_latex` FROM `wm_formula` "
               "ORDER BY `id` ASC")
        cursor.execute(sql)
        formulas = cursor.fetchall()
    else:
        formulas = filter_dataset.get_symbol_ids(dataset,
                                                 filter_dataset.get_metadata())
    return formulas
