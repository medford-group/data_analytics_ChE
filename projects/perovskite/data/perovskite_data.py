import matplotlib.pyplot as plt
import pandas as pd
import ase.db

con = ase.db.connect('cubic_perovskites.db')

df = pd.read_csv('perovskites.csv')

bgap_dict = {}

for row in con.select('combination'):
    formula = row.A_ion + row.B_ion + row.anion
    bgap_dict[formula] = row.gllbsc_dir_gap

n_r_dict = {}
for i, rowdf in df.iterrows():
    for ion in ['A', 'B', 'X']:
        ion_name = rowdf[ion]
        if ion not in n_r_dict:
            n_r_dict[ion_name] = [rowdf['n'+ion], rowdf['r'+ion+' (Ang)']]

k = 0
gaps = []
for i, rowdf in df.iterrows():
    name = rowdf['ABX3']
    if name in bgap_dict:
        gap = bgap_dict[name]
        gaps.append(gap)
    else:
        gaps.append('?')

df['Bandgap [eV]'] = gaps

for row in con.select('combination'):
    A = row.A_ion
    B = row.B_ion
    X = row.anion.replace('3','')
    gap = row.gllbsc_dir_gap
    if (A in n_r_dict) and (B in n_r_dict) and (X in n_r_dict) and (gap > 0):
        formula = A + B + X + '3'
        newrow = pd.DataFrame([[formula, A, B, X, n_r_dict[A][0], n_r_dict[B][0], n_r_dict[X][0], n_r_dict[A][1], n_r_dict[B][1], n_r_dict[X][1],'?', '?', '?', gap]], columns = df.columns)
        df = df.append(newrow)



df.to_csv('perovskites_gaps.csv')
