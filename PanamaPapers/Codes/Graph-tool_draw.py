import graph_tool.all as gt
import numpy as np
from math import sqrt

g = gt.Graph()

ID = g.new_vertex_property("int")
name =  g.new_vertex_property("string")
shape =  g.new_vertex_property("string")
country_codes =  g.new_vertex_property("string")
countries =  g.new_vertex_property("string")
type = g.new_vertex_property("string")
degrees = g.new_vertex_property("int")
subgraph = g.new_vertex_property("int")
color_bytype = g.new_vertex_property("vector<double>")
cmt = g.new_vertex_property("int")

edge_label = g.new_edge_property("string")
edge_color = g.new_edge_property("vector<double>")
edge_width = g.new_edge_property("int")
control = g.new_edge_property("vector<double>")

varry = np.load("Output_networks/Component2995nodes.npy",allow_pickle=True)
egdays = np.load("Output_networks/Component2995nodes_sfdp_edges.npy", allow_pickle=True)
g.add_vertex(len(varry))

color_edge_dict={"intermediary of":[0.980, 0.921, 0.2, 0.7], # yellow
                 "shareholder of":[0.478, 0.482, 1, 0.7], #purple
                 "beneficiary of":[.5, .5, .5, .7],
                 "registered address":[0.882, 0.443, 0.996, 0.7] # pinkish
                 }
width_edge_dict={"intermediary of":1, "shareholder of":1.3,
                 "beneficiary of":0.9, "registered address":1.2}
shape_node_dict = {"intermediary":"circle", "officer":"triangle",
                 "entity":"pentagon", "address":"square", "unknown":"hexagon"}

for i in range(len(varry)):
    ID[g.vertex(i)] = varry[i, 0]
    name[g.vertex(i)]= varry[i, 1]
    country_codes[g.vertex(i)]= varry[i, 2]
    countries[g.vertex(i)]= varry[i, 3]
    type[g.vertex(i)]= varry[i, 4]
    degrees[g.vertex(i)]= varry[i, 5]
    color_bytype[g.vertex(i)] = [x for x in varry[i, 6]]
    shape[g.vertex(i)] = shape_node_dict[varry[i, 4]]

g.vertex_properties["ID"] = ID
g.vertex_properties["name"] = name
g.vertex_properties["countries"] = countries
g.vertex_properties["country_codes"] = country_codes
g.vertex_properties["type"] = type
g.vertex_properties["degrees"] = degrees
g.vertex_properties["color_bytype"] = color_bytype
g.vertex_properties["subgraph"] = subgraph
g.vertex_properties["shape"] = shape


for j in range(len(egdays)):
    [s, t, link] = egdays[j,[0,1,2]]
    edge = g.add_edge(g.vertex(int(s)), g.vertex(int(t)))
    edge_color[edge] = color_edge_dict[link] #[x for x in color]
    edge_label[edge] = link
    edge_width[edge] = width_edge_dict[link]

g.edge_properties["edge_color"] = edge_color
g.edge_properties["edge_label"] = edge_label
g.edge_properties["edge_width"] = edge_width

print('global_clustering', gt.global_clustering(g))
print('assortativity out', gt.assortativity(g, "out"))  # correlations
print('assortativity in', gt.assortativity(g, "in"))
print('assortativity total', gt.assortativity(g, "total"))

g = gt.GraphView(g)

print('start drawing')

pos_fr = gt.fruchterman_reingold_layout(g, n_iter=1000)
g.vertex_properties["pos_fr"] = pos_fr
control = g.new_edge_property("vector<double>")
for e in g.edges():
     d = sqrt(sum((pos_fr[e.source()].a - pos_fr[e.target()].a) ** 2)) / 5
     control[e] = [0.3, d, 0.7, d]
g.edge_properties["control"] = control

gt.graph_draw(g, pos=pos_fr,
              vertex_pen_width=0.6, vertex_color=[1, 1, 1, 1],
              vertex_fill_color=color_bytype,
              vertex_size=gt.prop_to_size(degrees, mi=10, ma=20),
              edge_color=edge_color,
              edge_control_points=control,
              edge_pen_width=edge_width,
              output_size=(800, 800),
              output="Graphs/Component2995nodes_fr.svg")

pos_rt = gt.radial_tree_layout(g,  g.vertex(0))
for e in g.edges():
     d = sqrt(sum((pos_rt[e.source()].a - pos_rt[e.target()].a) ** 2)) / 5
     control[e] = [0.3, d, 0.7, d]
gt.graph_draw(g, pos=pos_rt,
              vertex_pen_width=0.6, vertex_color=[1, 1, 1, 1],
              vertex_fill_color=color_bytype,
              vertex_size=gt.prop_to_size(degrees, mi=10, ma=20),
              edge_color=edge_color,
              edge_control_points=control,
              edge_pen_width=edge_width,
              output_size=(800, 800),
              output="Graphs/Component2995nodes_rt.svg")