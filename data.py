import torch
import os
from datetime import datetime
import time
import random
import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def data_init():
    print("Data Initialization......")
    continents = pd.read_csv('./data/continents2.csv').fillna(0)
    country_pop = pd.read_csv('./data/population_by_country_2020.csv').fillna(0)
    death_air = pd.read_csv('./data/death-rates-from-air-pollution.csv').fillna(0)
    death_by_factor = pd.read_csv('./data/number-of-deaths-by-risk-factor.csv').fillna(0)

    name = []
    code = []
    region = []
    sub_region = []
    population = []
    density = []
    land_area = []
    fert_rate = []
    urban_pop = []
    Years = []
    deaths = []
    household = []
    ambient_matter = []
    ambient_ozone = []
    air_polution = []
    outdoor_air_pol = []

    for i in tqdm(range(death_air.shape[0])):
        obj = death_air.iloc[i]
        fac = death_by_factor.iloc[i]
        tmp = continents[continents['name'] == obj['Entity']]
        tmp1 = country_pop[country_pop['Country'] == obj['Entity']]
        if (tmp1.shape[0] == 1 and tmp.shape[0] ==1 and fac['Entity'] == obj['Entity'] and fac['Year'] == obj['Year']):
            td = tmp.iloc[0]
            td1 = tmp1.iloc[0]
            name.append(obj['Entity'])
            code.append(obj['Code'])
            region.append(td['region'])
            sub_region.append(td['sub-region'])
            population.append(td1['Population'])
            density.append(td1['Density'])
            land_area.append(td1['Land_Area'])
            if (td1['Fert_Rate'] == 'N.A.'):
                fert_rate.append(0.0)
            else: 
                fert_rate.append(float(td1['Fert_Rate']))
            if (td1['Urban_Pop'] == 'N.A.'):
                urban_pop.append(0)
            else: 
                urban_pop.append(((float)(td1['Urban_Pop'][0:len(td1['Urban_Pop'])-2])))
            Years.append(obj['Year'])
            deaths.append(obj['Deaths'])
            household.append(obj['Household'])
            ambient_matter.append(obj['Ambient_matter'])
            ambient_ozone.append(obj['Ambient_ozone'])
            air_polution.append(fac['Air_pollution'])
            outdoor_air_pol.append(fac['Outdoor_air_pollution'])

    df = pd.DataFrame({
        'Country': name,
        'Coutry Code': code,
        'Region': region,
        'Sub-Region': sub_region,
        'Population': population, #int
        'Density': density, #int
        'Land Area': land_area, #int
        'Fert Rate': fert_rate,  #percentage
        'Urban Pop': urban_pop, #percentage
        'Years': Years, #category
        'Deaths': deaths, #int
        'Household Pollution': household,  #float
        'Ambient Matter Pollution': ambient_matter, #float
        'Ambient Ozone Pollution': ambient_ozone, #float
        'Air Pollution': air_polution, #float
        'Outdoor Air Pollution': outdoor_air_pol #float
    })
    return df
if __name__ == '__main__':
    data_init()