import matplotlib.pyplot as plt
import networkx as nx
from scipy.cluster import hierarchy
from scipy.spatial import distance
from collections import defaultdict
import numpy
import sys
import copy
import random
from sklearn.cluster import DBSCAN, KMeans
from gensim.models import Doc2Vec
from os import listdir
from os.path import isfile, join
import numpy as np
import nltk
from gensim import utils
import random
import infomap
import igraph as ig


def load_tsne_coordinates_from(filename):
    file = open(filename)
    lines = file.readlines()

    line_xy_dict = {}
    line_to_xy_dict = {}
    for line in lines:
        row = line.split()
        x = float(row[0])
        y = float(row[1])
        try:
            line_id = row[2]
        except:
            continue
        line_xy_dict[line_id] = (x,y)
        line_to_xy_dict[(x, y)] = line_id

    return line_xy_dict, line_to_xy_dict


line_xy_dict, line_to_xy_dict = load_tsne_coordinates_from ('results/tsne_coordinates.txt')
model = Doc2Vec.load('lines-150.d2v')
path = 'ordered_lines.txt'
lines = [line for line in open(path, encoding = "ISO-8859-1").readlines()]
doc_ids = sorted(list(model.docvecs.doctags.keys()))

NUM_CLUSTERS = 1500
WEIGTH_THRESHOLD = 1 #len(doc_ids)/NUM_CLUSTERS/100
print('The weigth threshold is', WEIGTH_THRESHOLD)
all_edges = []

for i in range(len(doc_ids)-1):
    all_edges.append ((doc_ids[i],doc_ids[i+1]))

g = nx.Graph()
g.add_nodes_from(doc_ids)
g.add_edges_from(all_edges)

print('Performing KMeans')
xy_list = [line_xy_dict[ident] for ident in doc_ids]
sklearn_clusters = KMeans(n_clusters=NUM_CLUSTERS, n_jobs=1).fit(xy_list)
xy_list_dict = {}
for i, label in enumerate(sklearn_clusters.labels_):
    try:
        xy_list_dict[label].append(line_to_xy_dict[xy_list[i]])
    except:
        xy_list_dict[label] = [line_to_xy_dict[xy_list[i]]]

nodes_chunks = []
for key in xy_list_dict.keys():
    nodes_chunks.append(xy_list_dict[key])

new_line_xy_dict = {}
cluster_dict = {}
for i, chunk in enumerate(nodes_chunks):
    coordinates = [line_xy_dict [ident] for ident in chunk]
    com = numpy.sum(coordinates,0)/len(coordinates)
    new_line_xy_dict [i] = com
    cluster_dict [i] = chunk

print('Performing blockmodels')
blocks_graph = nx.blockmodel (g, nodes_chunks, multigraph = True)
g = blocks_graph
nx.draw(g,new_line_xy_dict, node_shape = '.', alpha=0.002)
plt.show()
    

edges = g.edges()
edges_weigth = {}
for e in edges:
    try:
        edges_weigth[e] += 1
    except:
        edges_weigth[e] = 1

new_edges = []
for e, weigth in edges_weigth.items():
    if weigth < WEIGTH_THRESHOLD:
        continue
    new_edges.append(e)

g = nx.Graph()
g.add_nodes_from(doc_ids)
g.add_edges_from(new_edges)
        
i = 0
biggest_clusters = []
for key in clusters.keys():
    cluster = clusters[key]
    new_cluster = []
    for item in cluster:
        print(item)
        new_cluster += cluster_dict[item]
    try:
        biggest_clusters.find(cluster)
        continue
    except:
        pass
    biggest_clusters.append(new_cluster)
    gg = nx.Graph()
    gg.add_nodes_from (new_cluster)
    nx.draw(gg, line_xy_dict, node_shape = '.', linewidths = 0, node_size=10, node_color=colors[i%len(colors)])
    i += 1
plt.show()

print('---')
file = open ('results/edges.txt', 'w')
matching_labels = 0
tot_labels = 0
for e, weigth in edges_weigth.items():
    if weigth < WEIGTH_THRESHOLD:
        continue
    from_vertex = e[0]
    to_vertex = e[1]
    from_cluster = cluster_dict[from_vertex]
    to_cluster = cluster_dict[to_vertex]
    file.write (str(from_vertex) + ';')
    file.write (str(from_cluster).replace('[','').replace(']','').strip())
    file.write (';' + str(to_vertex) + ';')
    file.write (str(to_cluster).replace('[','').replace(']','').strip())
    file.write (';' + str(weigth) + '\n')
    print(len(from_cluster))

