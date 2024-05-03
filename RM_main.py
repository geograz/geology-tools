# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 14:00:44 2021
author: Georg H. Erharter

Python script that computes rockmass parameters for a set of multiple input
parameters based on the Hoek Brown failure criterion. An application would be
if multiple sets of rockmass parameters for different overburdens and / or
different levels of rockmass disturbance should be computed. The code creates
two excel files where one contains the input parameters and one the output
parameters.

Code requires the custom library "RM_lib.py" to work.

No guarantee is given on the flawless functionality of the code and the code is
licensed under the MIT License (see license file in repository).
Parts of the code are based on: http://geologyandpython.com/hoek-brown.html
"""

import pandas as pd

from RM_lib import Hoek, Utilities, Deformation

hoek = Hoek()
utils = Utilities()
deform = Deformation()


###############################################################################
# dictionary with input parameters of rockmass type to test

NAME = 'rt1'  # name of rockmass type and filename to save results
inputs = {'intact UCS [MPa]': [30, 35],  # sigci
          'GSI': [50],  # GSI
          'mi': [12],  # mi
          'disturbance factor': [0.0, 0.2],  # D
          'intact modulus - Ei [MPa]': [12000],  # Ei
          'unit weight [MN/m³]': [0.026],  # unit weight
          'tunnel depth [m]': [10, 50, 100]}  # tunnel depth / overburden


###############################################################################
# compute rockmass parameters for all possible parameter combinations

df_combinations = utils.get_combinations(inputs, NAME)

# create new dataframe that collects results
df_output = pd.DataFrame({'mb': [], 's': [], 'a': [], 'sig3max [MPa]': [],
                          'cohesion [MPa]': [], 'friction angle [°]': [],
                          'RM tensile strength [MPa]': [], 'RM UCS [MPa]': [],
                          'RM global strength [MPa]': [],
                          'RM DefMod Hoek&al2002 [MPa]': [],
                          'RM DefMod Hoek&Diederichs2006 [MPa]': [],
                          'RM DefMod Verman&al1997': [],
                          'RM DefMod Asef&Reddish2002 [MPa]': []
                          })

# main loop that iterates through all possible combinations
for i in df_combinations.index:
    print(f'combination: {i}')
    c = df_combinations.iloc[i]

    mb, s, a = hoek.HoekBrownCriterion(c['mi'], c['GSI'],
                                       c['disturbance factor'])

    sigcm, sig3_max = hoek.FailureEnvelopeRange(c['intact UCS [MPa]'], mb, s,
                                                a, c['unit weight [MN/m³]'],
                                                c['tunnel depth [m]'])

    phi, coh = hoek.MohrCoulombFit(sig3_max, c['intact UCS [MPa]'], a, mb, s)

    sigc, sigtm = hoek.RMStrength(c['intact UCS [MPa]'], s, a, mb)

    ERM_Hoek_0 = deform.RMDef_Hoek(c['intact UCS [MPa]'],
                                   c['disturbance factor'],
                                   c['GSI'], c['intact modulus - Ei [MPa]'],
                                   paper='Hoek et al. (2002)')

    ERM_Hoek_1 = deform.RMDef_Hoek(c['intact UCS [MPa]'],
                                   c['disturbance factor'],
                                   c['GSI'], c['intact modulus - Ei [MPa]'],
                                   paper='Hoek & Diederichs (2006)')

    ERM_Verman = deform.RMDef_Verman1997(c['GSI'], c['tunnel depth [m]'])

    ERM_AsefReddish2002 = deform.RMDef_AsefReddish2002(
        c['intact UCS [MPa]'], 400, sigc, c['unit weight [MN/m³]'],
        c['tunnel depth [m]'], k0=0.33)

    df_temp = pd.DataFrame(
        {'mb': [mb], 's': [s], 'a': [a],
         'sig3max [MPa]': [sig3_max],
         'cohesion [MPa]': [coh],
         'friction angle [°]': [phi],
         'RM tensile strength [MPa]': [sigtm],
         'RM UCS [MPa]': [sigc],
         'RM global strength [MPa]': [sigcm],
         'RM DefMod Hoek&al2002 [MPa]': [ERM_Hoek_0],
         'RM DefMod Hoek&Diederichs2006 [MPa]': [ERM_Hoek_1],
         'RM DefMod Verman&al1997': [ERM_Verman],
         'RM DefMod Asef&Reddish2002 [MPa]': [ERM_AsefReddish2002]})
    df_output = pd.concat([df_output, df_temp])

df_output.index = df_combinations.index
# save results to excel file
df_output.to_excel(f'{NAME}_output.xlsx', index=True)
