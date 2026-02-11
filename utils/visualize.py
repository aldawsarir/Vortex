import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import os

def create_mindmap(keywords):
    G = nx.Graph()
    center = "Main Topic"
    
    for word in keywords:
        if word:
            G.add_edge(center, word)
    
    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        with_labels=True,
        node_color='#6C63FF',
        node_size=3000,
        font_size=10,
        font_weight='bold'
    )
    
    output_path = os.path.join('static', 'images', 'mindmap.png')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()