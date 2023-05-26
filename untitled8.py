# -*- coding: utf-8 -*-
"""
Created on Wed May 17 09:39:11 2023

@author: ZAM0335
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense

df = pd.read_csv('Tenor_by_Division_Full_Data_data.csv')