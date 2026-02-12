import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import os

def create_mindmap(keywords):
    """
    Create a beautiful mind map with Pastel Illustration Theme colors
    """
    G = nx.Graph()
    center = "Main Topic"
    
    # Add edges between center and keywords
    for word in keywords:
        if word and word.strip():
            G.add_edge(center, word)
    
    # Create figure with better size
    plt.figure(figsize=(12, 8), facecolor='#E8D5F2')  # Pastel lavender background
    
    # Layout - spring layout for better distribution
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Draw edges with Pastel colors
    nx.draw_networkx_edges(
        G, pos,
        edge_color='#C4A7D7',  # Pastel purple
        width=3,
        alpha=0.6
    )
    
    # Prepare node colors - center node different from keywords
    node_colors = []
    for node in G.nodes():
        if node == center:
            node_colors.append('#5DBAA4')  # Teal for center
        else:
            node_colors.append('#6BA3C8')  # Blue for keywords
    
    # Draw nodes with Pastel colors
    nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        node_size=4000,
        alpha=0.9,
        edgecolors='#FFFFFF',  # White border
        linewidths=3
    )
    
    # Draw labels with better styling
    nx.draw_networkx_labels(
        G, pos,
        font_size=12,
        font_weight='bold',
        font_color='#FFFFFF',  # White text
        font_family='sans-serif'
    )
    
    # Remove axes
    plt.axis('off')
    
    # Add title
    plt.title(
        '🧠 Mind Map',
        fontsize=20,
        fontweight='bold',
        color='#2C2C54',
        pad=20
    )
    
    # Save with high quality
    output_path = os.path.join('static', 'images', 'mindmap.png')
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(
        output_path,
        bbox_inches='tight',
        dpi=150,  # High quality
        facecolor='#E8D5F2',  # Pastel background
        edgecolor='none'
    )
    plt.close()
    
    return output_path


def create_simple_mindmap(keywords):
    """
    Alternative simple version with circular layout
    """
    G = nx.Graph()
    center = "Main Topic"
    
    for word in keywords:
        if word and word.strip():
            G.add_edge(center, word)
    
    plt.figure(figsize=(10, 8), facecolor='#E8D5F2')
    
    # Circular layout
    pos = nx.circular_layout(G)
    
    # Center the main topic
    pos[center] = [0, 0]
    
    # Draw with Pastel colors
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=['#5DBAA4' if node == center else '#FFB3BA' for node in G.nodes()],
        node_size=[5000 if node == center else 3500 for node in G.nodes()],
        font_size=11,
        font_weight='bold',
        font_color='white',
        edge_color='#C4A7D7',
        width=2.5,
        alpha=0.9,
        edgecolors='white',
        linewidths=2
    )
    
    plt.axis('off')
    plt.title('🧠 Mind Map', fontsize=18, fontweight='bold', color='#2C2C54', pad=15)
    
    output_path = os.path.join('static', 'images', 'mindmap.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(output_path, bbox_inches='tight', dpi=150, facecolor='#E8D5F2')
    plt.close()
    
    return output_path


def create_hierarchical_mindmap(keywords):
    """
    Hierarchical tree-style mind map
    """
    G = nx.DiGraph()  # Directed graph for hierarchy
    center = "Main Topic"
    
    for word in keywords:
        if word and word.strip():
            G.add_edge(center, word)
    
    plt.figure(figsize=(12, 10), facecolor='#E8D5F2')
    
    # Tree layout
    pos = nx.spring_layout(G, k=3, iterations=100)
    
    # Draw nodes with gradient colors
    pastel_colors = ['#5DBAA4', '#6BA3C8', '#FFB3BA', '#FFD166', '#C4A7D7', '#7DD3BD']
    
    node_colors = []
    for i, node in enumerate(G.nodes()):
        if node == center:
            node_colors.append('#5DBAA4')
        else:
            node_colors.append(pastel_colors[i % len(pastel_colors)])
    
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=4500,
        font_size=11,
        font_weight='bold',
        font_color='white',
        edge_color='#C4A7D7',
        width=3,
        alpha=0.85,
        arrows=False,
        edgecolors='white',
        linewidths=2.5
    )
    
    plt.axis('off')
    plt.title('🧠 Mind Map - Hierarchical View', fontsize=20, fontweight='bold', color='#2C2C54', pad=20)
    
    output_path = os.path.join('static', 'images', 'mindmap.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(output_path, bbox_inches='tight', dpi=150, facecolor='#E8D5F2')
    plt.close()
    
    return output_path