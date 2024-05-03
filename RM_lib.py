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

"RM_lib.py" is the custom library for the file "RM_main.py".

No guarantee is given on the flawless functionality of the code and the code is
licensed under the MIT License (see license file in repository).
Parts of the code are based on: http://geologyandpython.com/hoek-brown.html
"""

from itertools import product
import numpy as np
import pandas as pd


class Utilities:
    '''class that contains general purpose functions'''

    def get_combinations(self, dictionary: dict, name: str) -> pd.DataFrame:
        '''compute all possible combinations of lists that are
        values of a dictionary'''
        combinations = list(product(*list(
            [dictionary['intact UCS [MPa]'],
             dictionary['GSI'],
             dictionary['mi'],
             dictionary['disturbance factor'],
             dictionary['intact modulus - Ei [MPa]'],
             dictionary['unit weight [MN/m³]'],
             dictionary['tunnel depth [m]']])))
        # save combinations
        df = pd.DataFrame(np.array(combinations), columns=dictionary.keys())
        df.to_excel(f'{name}_input.xlsx', index=True)
        return df


class Hoek:
    '''class for computation of the Hoek Brown failure criterium according to
    Hoek, E., Carranza-Torres, C. and Corkum, B. (2002),
    “Hoek-Brown failure criterion – 2002 Edition”, Toronto.'''

    def __init__(self):
        pass

    def HoekBrownCriterion(self, mi: int, GSI: int, D: float) -> list:
        '''equations 3, 4, 5 of Hoek et al. (2002);
        see e.g. Hoek and Brown (1997) Practical estimates of rock mass
        strength for mi values'''
        mb = mi * np.exp((GSI-100)/(28-(14*D)))
        s = np.exp((GSI-100)/(9-(3*D)))
        a = (1/2)+(1/6)*(np.exp(-GSI/15)-np.exp(-20/3))
        return mb, s, a

    def FailureEnvelopeRange(self, sigci: float, mb: float, s: float, a: float,
                             unit_weigth: float, depth: float) -> list:
        sigcm = sigci * (mb+4*s-a*(mb-8*s))*(((mb/4)+s)**(a-1))/(2*(1+a)*(2+a))
        sig3_max = sigcm * 0.47 * (sigcm / (unit_weigth * depth))**(-.94)
        return sigcm, sig3_max

    def MohrCoulombFit(self, sig3_max: float, sigci: float, a: float,
                       mb: float, s: float) -> list:
        sig3n = sig3_max / sigci
        phi = np.rad2deg(np.arcsin((6*a*mb*((s+mb*sig3n)**(a-1)))/(2*(1+a)*(2+a)+6*a*mb*((s+mb*sig3n)**(a-1)))))

        coh_term1 = sigci*((1+2*a)*s+(1-a)*mb*sig3n)*((s+mb*sig3n)**(a-1))
        coh_term2 = (1+a)*(2+a)*np.sqrt(1+(6*a*mb*((s+mb*sig3n)**(a-1)))/((1+a)*(2+a)))
        coh = coh_term1 / coh_term2
        return phi, coh

    def RMStrength(self, sigci: float, s: float, a: float, mb: float) -> list:
        sigc = sigci*s**a
        sigtm = (s * sigci)/mb*-1
        return sigc, sigtm


class Deformation:
    '''class that contains functions to compute the rockmass deformation moduli
    according to various authors'''

    def __init__(self):
        pass

    def RMDef_Hoek(self, sigci: float, D: float, GSI: int, Ei: float,
                   paper='Hoek & Diederichs (2006)') -> float:
        '''2 ways to compute the rockmass deformation modulus acc. to Hoek are
        implemented:
        Hoek, E., Carranza-Torres, C. and Corkum, B. (2002),
        “Hoek-Brown failure criterion – 2002 Edition”, Toronto.

        and the improved version:
        Hoek, E. and Diederichs, M.S. (2006), “Empirical estimation of rock
        mass modulus”, International Journal of Rock Mechanics and Mining
        Sciences, Vol. 43 No. 2, pp. 203–215.'''
        if paper == 'Hoek et al. (2002)':
            # rockmass deformation modulus after Hoek et al. (2002)
            Erm = (1 - (D/2)) * (np.sqrt(sigci/100.0)*10**((GSI-10)/40.0)) * 10**3
        elif paper == 'Hoek & Diederichs (2006)':
            # rockmass deformation modulus after Hoek & Diederichs (2006)
            Erm = Ei*(0.02+((1-D/2)/(1+np.exp((60+15*D-GSI)/11))))
        return Erm

    def RMDef_Arora1987(self):
        '''not yet implemented way to compute the rockmass deformation modulus
        acc. to
        Arora, Vijay Kumar. “Strength and deformational behaviour of jointed
        rocks.” (1987).'''
        pass

    def RMDef_Verman1997(self, GSI, depth):
        '''computation of the rockmass deformation modulus acc. to
        Verman, Manoj, Bhawani Singh, M. N. Viladkar and Jaydev Jethwa. “Effect
        of tunnel depth on modulus of deformation of rock mass.” Rock Mechanics
        and Rock Engineering 30 (1997): 121-127.'''
        RMR = GSI  # according to Saroglou et al. 2019
        # alpha = 0.3 and 0.16 at RMR = 68 and 31, respectively
        alpha = np.interp(RMR, [31, 68], [0.16, 0.3])
        Erm = 0.4*(depth**alpha)*10**((RMR-20)/38)  # GPa
        return Erm * 1000  # MPa

    def RMDef_AsefReddish2002(self, sigc, E_0, sig_cm, unit_weigth, depth,
                              k0):
        '''computation of the rockmass deformation modulus acc. to
        Asef, Mohammad Reza and David J. Reddish. “The impact of confining
        stress on the rock mass deformation modulus.” Geotechnique 52 (2002):
        235-241.'''
        # sigc: unconfined compressive strength of the intact rock
        # E_0: deformation modulus of the jointed rock mass at UCS
        # sig3: sigma3 = sigma2 triaxial stress
        # sig_cm: unconfined compressive strength of the jointed rock mass
        sig1 = unit_weigth * depth
        sig3 = sig1 * k0

        b = 15 + 60*np.exp(-0.18*sigc)
        term1 = 200*(sig3 / sig_cm) + b

        term2 = (sig3 / sig_cm) + b
        Erm = (E_0/1000) * (term1 / term2)
        return Erm * 1000


if __name__ == '__main__':
    # example usage to determine mb, s, a

    mi = 10
    GSI = 70
    D = 0

    hoek = Hoek()
    mb, s, a = hoek.HoekBrownCriterion(mi, GSI, D)

    print(f'mb: {round(mb, 2)}, s: {round(s, 2)}, a: {round(a, 2)}')
