# -*- coding: utf-8 -*-
"""
    This file is part of egg-force-one.

    egg-force-one is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with egg-force-one.  If not, see <http://www.gnu.org/licenses/>. 2

    ############################################################################

    Created on Mon Sep 25 16:24:39 2017
    @author: CASAL Guillaume
"""

def allVarModule (module):
    """
    permet de connaitre les variable et les valeur dans un module
    """
    tempData = vars(module)
    tempName = dir(module)
    tempAll = []
    for var in tempName:
        if var[0] != '_':
            #print("{} : {}".format(var, tempData[var]))
            tempAll.append([var, tempData[var]])
            pass
        pass
    return tempAll

if __name__ == "__main__":
    import sysVar
    test = allVarModule(sysVar)
    for var in test:
        print(var)
    pass