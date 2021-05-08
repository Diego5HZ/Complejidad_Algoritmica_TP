!git clone https://github.com/lmcanavals/algorithmic_complexity.git 1>/dev/null

from algorithmic_complexity.aclib import graphstuff as gs
import pandas as pd
import numpy as np
import networkx as nx
import heapq as hq
import math

no_type_checking = ''
nom_departamento = 'AMAZONAS'
nom_provincia = 'UTCUBAMBA'
nom_distrito = 'CUMBA'
nom_centro_pob = 'CHALA'


url="https://raw.githubusercontent.com/lmcanavals/algorithmic_complexity/main/data/poblaciones.csv"
poblacionesDF = pd.read_csv(url)

nomdepartamentos = poblacionesDF['DEPARTAMENTO'].unique()

departamentos = dict()
for nom in nomdepartamentos:
  departamentos[nom] = poblacionesDF[poblacionesDF['DEPARTAMENTO'] == nom]

nomprovincias = departamentos[nom_departamento]['PROVINCIA'].unique()

provincias = dict()
for nom in nomprovincias:
  provincias[nom] = departamentos[nom_departamento][departamentos[nom_departamento]['PROVINCIA'] == nom]

nomdistritos = provincias[nom_provincia]['DISTRITO'].unique()

distritos = dict()
for nom in nomdistritos:
  distritos[nom] = provincias[nom_provincia][provincias[nom_provincia]['DISTRITO'] == nom]

distrito = distritos[nom_distrito]

def haversine(cp1, cp2):
  la1, lo1 = float(cp1['LATITUD']), float(cp1['LONGITUD'])
  la2, lo2 = float(cp2['LATITUD']), float(cp2['LONGITUD'])
  
  lo1, la1, lo2, la2 = map(math.radians, [lo1, la1, lo2, la2])
  dlo = lo2 - lo1
  dla = la2 - la1
  a = math.sin(dla/2)**2 + math.cos(la1) * math.cos(la2) * math.sin(dlo/2)**2
  c = 2 * math.asin(math.sqrt(a))
  r = 6371

  return round(c * r, 2)

G = nx.Graph()
col = 'CENTRO POBLADO'
for i, cp1 in distrito.iterrows():
  G.add_node(i, label=cp1[col])

for i, cp1 in distrito.iterrows():
  for j, cp2 in distrito.iterrows():
    if cp1[col] != cp2[col]:
      G.add_edge(i, j, weight=haversine(cp1, cp2))

#Dibujar grafo
gs.nx2gv(G, weighted=True, params={'size':'10'}, nodeinfo=True)

#Aplicación Dijkstra
G1 = nx.Graph()

def _dijkstra1(G, s, pobls, first):
  pob = -1
  largo=10000
  for v in G.neighbors(s):
    if G.edges[s, v]['weight'] < largo and v in pobls:
      largo, pob = G.edges[s, v]['weight'], v
          
  pobls.remove(s)
  if pobls:
    G1.add_node(s, label=G.nodes[s]['label'])
    G1.add_edge(s, pob, weight=largo)
    _dijkstra1(G, pob, pobls, first)
  else:
    G1.add_node(s, label=G.nodes[s]['label'])
    G1.add_edge(s, first, weight=G.edges[s, first]['weight'])

def dijkstra1(G, s):
  pobls = []
  first = -1
  for i, cp1 in distrito.iterrows():
    if cp1[col] == s:
      first=i
      break
  for u in G.nodes:
    pobls.append(u)

  _dijkstra1(G, first, pobls, first)

dijkstra1(G, nom_centro_pob)
#Dibujar ruta más corta
gs.nx2gv(G1, weighted=True, params={'size':'5'}, nodeinfo=True)
