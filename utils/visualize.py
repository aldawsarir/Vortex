import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import os
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.path import Path
import matplotlib.patches as patches

def create_mindmap(keywords):
    """
    Create a DETAILED mind map with main topics, subtopics, and connections
    Features: 3 levels (Center -> Main Topics -> Subtopics), curved edges, shadows, legend
    """
    if not keywords or len(keywords) == 0:
        keywords = ['Learning', 'Knowledge', 'Education', 'Growth', 'Success', 'Innovation']
    
    # Create graph
    G = nx.Graph()
    center = "Main\nTopic"
    
    # Add main branches (keywords) - LEVEL 1
    main_topics = []
    for i, word in enumerate(keywords[:6]):  # Limit to 6 main topics
        if word and word.strip():
            main_topics.append(word)
            G.add_edge(center, word)
    
    # Add SUBTOPICS for each main topic - LEVEL 2 (THIS MAKES IT DETAILED!)
    subtopics_map = {
        0: ['Definition', 'Examples', 'Benefits'],
        1: ['Methods', 'Tools', 'Resources'],
        2: ['Practice', 'Theory', 'Application'],
        3: ['Key Points', 'Summary', 'Overview'],
        4: ['Details', 'Analysis', 'Insights'],
        5: ['Concepts', 'Ideas', 'Principles']
    }
    
    for i, main_topic in enumerate(main_topics):
        # Add 3 subtopics for each main topic
        subtopics = subtopics_map.get(i, ['Detail 1', 'Detail 2', 'Detail 3'])
        for j, subtopic in enumerate(subtopics[:3]):
            subtopic_name = f"{subtopic}"
            G.add_edge(main_topic, subtopic_name)
    
    # Create figure - LARGER for more details
    fig, ax = plt.subplots(figsize=(20, 16), facecolor='#E8D5F2')
    ax.set_facecolor('#E8D5F2')
    
    # Spring layout with MORE spacing
    pos = nx.spring_layout(G, k=1.5, iterations=150, seed=42)
    
    # Scale positions for better visibility
    for node in pos:
        pos[node] = pos[node] * 2.5
    
    # Pastel color palette
    pastel_colors = [
        '#FFB3BA',  # Pink
        '#FFDFBA',  # Peach
        '#BAFFC9',  # Mint
        '#BAE1FF',  # Sky Blue
        '#E0BBE4',  # Lavender
        '#FFDFD3',  # Coral
        '#C9E4DE',  # Seafoam
        '#F8E6FF',  # Light Purple
    ]
    
    # Draw edges with DIFFERENT styles based on level
    for edge in G.edges():
        node1, node2 = edge
        x1, y1 = pos[node1]
        x2, y2 = pos[node2]
        
        # Determine edge type
        if node1 == center or node2 == center:
            # Main topic connection - THICK & TEAL
            color = '#5DBAA4'
            width = 6
            alpha = 0.8
        else:
            # Subtopic connection - THIN & PURPLE
            color = '#C4A7D7'
            width = 3
            alpha = 0.5
        
        # Create curved path
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 + 0.15
        
        verts = [(x1, y1), (mid_x, mid_y), (x2, y2)]
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        
        path = Path(verts, codes)
        patch_line = patches.PathPatch(
            path, 
            facecolor='none', 
            edgecolor=color, 
            lw=width, 
            alpha=alpha,
            zorder=1
        )
        ax.add_patch(patch_line)
    
    # Draw nodes with DIFFERENT sizes based on level
    node_index = 0
    for node in G.nodes():
        x, y = pos[node]
        
        if node == center:
            # CENTER NODE - LARGEST
            size = 0.35
            color = '#5DBAA4'
            border_width = 8
            font_size = 20
            text_color = 'white'
            
        elif node in main_topics:
            # MAIN TOPICS - MEDIUM
            size = 0.25
            color = pastel_colors[node_index % len(pastel_colors)]
            border_width = 6
            font_size = 14
            text_color = 'white'
            node_index += 1
            
        else:
            # SUBTOPICS - SMALL
            size = 0.18
            color = '#FFE4E1'  # Light pink for subtopics
            border_width = 4
            font_size = 10
            text_color = '#2C2C54'
        
        # Shadow
        shadow = Circle(
            (x - 0.02, y - 0.02), 
            size, 
            facecolor='gray', 
            alpha=0.25,
            zorder=2
        )
        ax.add_patch(shadow)
        
        # Main circle
        circle = Circle(
            (x, y), 
            size, 
            facecolor=color, 
            edgecolor='white', 
            linewidth=border_width,
            zorder=3,
            alpha=0.95
        )
        ax.add_patch(circle)
        
        # Inner glow for center and main topics
        if node == center or node in main_topics:
            glow = Circle(
                (x, y), 
                size + 0.02, 
                facecolor='none', 
                edgecolor='white', 
                linewidth=2,
                alpha=0.4,
                zorder=4
            )
            ax.add_patch(glow)
        
        # Label with word wrapping
        label_text = node
        if len(label_text) > 15 and node not in [center]:
            # Split long text
            words = label_text.split()
            if len(words) > 1:
                mid = len(words) // 2
                label_text = ' '.join(words[:mid]) + '\n' + ' '.join(words[mid:])
        
        ax.text(
            x, y, 
            label_text, 
            fontsize=font_size, 
            fontweight='bold',
            ha='center', 
            va='center',
            color=text_color,
            zorder=5,
            family='sans-serif'
        )
    
    # Add LEGEND
    legend_elements = [
        Circle((0, 0), 0.1, facecolor='#5DBAA4', edgecolor='white', linewidth=3, label='Main Topic'),
        Circle((0, 0), 0.1, facecolor='#FFB3BA', edgecolor='white', linewidth=3, label='Key Concepts'),
        Circle((0, 0), 0.1, facecolor='#FFE4E1', edgecolor='white', linewidth=3, label='Details')
    ]
    
    legend = ax.legend(
        handles=legend_elements,
        loc='upper right',
        fontsize=14,
        frameon=True,
        facecolor='white',
        edgecolor='#C4A7D7',
        framealpha=0.9,
        shadow=True
    )
    legend.set_zorder(10)
    
    # Title with INFO
    total_nodes = G.number_of_nodes()
    total_edges = G.number_of_edges()
    subtopics_count = total_nodes - len(main_topics) - 1
    
    plt.title(
        f'🧠 Detailed Mind Map\n{len(main_topics)} Main Topics • {subtopics_count} Subtopics', 
        fontsize=30, 
        fontweight='bold', 
        color='#2C2C54', 
        pad=40,
        family='sans-serif'
    )
    
    # Add decorative border
    border = FancyBboxPatch(
        (0.01, 0.01), 
        0.98, 
        0.98,
        boxstyle="round,pad=0.02",
        edgecolor='#C4A7D7',
        facecolor='none',
        linewidth=5,
        transform=ax.transAxes,
        zorder=0,
        alpha=0.6
    )
    ax.add_patch(border)
    
    # Add FOOTER with statistics
    footer_text = f"📊 Total Nodes: {total_nodes} | Total Connections: {total_edges} | Levels: 3"
    ax.text(
        0.5, -0.05,
        footer_text,
        transform=ax.transAxes,
        fontsize=16,
        ha='center',
        color='#2C2C54',
        fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#C4A7D7', alpha=0.8)
    )
    
    # Remove axes
    ax.axis('off')
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    
    # Save with VERY high quality
    output_path = os.path.join('static', 'images', 'mindmap.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(
        output_path, 
        bbox_inches='tight', 
        dpi=250,  # VERY HIGH DPI
        facecolor='#E8D5F2',
        edgecolor='none',
        pad_inches=0.5
    )
    plt.close()
    
    print(f"✅ DETAILED mind map created: {total_nodes} nodes, {total_edges} connections, {subtopics_count} subtopics")
    return output_path


def create_simple_mindmap(keywords):
    """
    Alternative simple version with circular layout and enhanced styling
    """
    if not keywords or len(keywords) == 0:
        keywords = ['Learning', 'Knowledge', 'Education']
    
    G = nx.Graph()
    center = "Main Topic"
    
    for word in keywords:
        if word and word.strip():
            G.add_edge(center, word)
    
    fig, ax = plt.subplots(figsize=(12, 9), facecolor='#E8D5F2')
    ax.set_facecolor('#E8D5F2')
    
    # Circular layout
    pos = nx.circular_layout(G)
    pos[center] = [0, 0]  # Center the main topic
    
    # Draw edges with gradient effect
    nx.draw_networkx_edges(
        G, pos,
        edge_color='#C4A7D7',
        width=4,
        alpha=0.5,
        ax=ax
    )
    
    # Node colors
    node_colors = ['#5DBAA4' if node == center else '#FFB3BA' for node in G.nodes()]
    node_sizes = [6000 if node == center else 4000 for node in G.nodes()]
    
    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        node_size=node_sizes,
        alpha=0.9,
        edgecolors='white',
        linewidths=4,
        ax=ax
    )
    
    # Draw labels
    nx.draw_networkx_labels(
        G, pos,
        font_size=12,
        font_weight='bold',
        font_color='white',
        font_family='sans-serif',
        ax=ax
    )
    
    ax.axis('off')
    plt.title(
        '🧠 Mind Map - Circular View', 
        fontsize=22, 
        fontweight='bold', 
        color='#2C2C54', 
        pad=25
    )
    
    output_path = os.path.join('static', 'images', 'mindmap.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(
        output_path, 
        bbox_inches='tight', 
        dpi=180, 
        facecolor='#E8D5F2'
    )
    plt.close()
    
    return output_path


def create_hierarchical_mindmap(keywords):
    """
    Hierarchical tree-style mind map with enhanced visuals
    """
    if not keywords or len(keywords) == 0:
        keywords = ['Learning', 'Knowledge', 'Education']
    
    G = nx.DiGraph()  # Directed graph
    center = "Central\nIdea"
    
    for word in keywords[:7]:  # Limit for clarity
        if word and word.strip():
            G.add_edge(center, word)
    
    fig, ax = plt.subplots(figsize=(16, 12), facecolor='#E8D5F2')
    ax.set_facecolor('#E8D5F2')
    
    # Tree layout
    pos = nx.spring_layout(G, k=2.8, iterations=120, seed=42)
    
    # Pastel colors rotation
    pastel_colors = [
        '#5DBAA4', '#6BA3C8', '#FFB3BA', '#FF9AA2', 
        '#FFD166', '#C4A7D7', '#7DD3BD', '#BAFFC9'
    ]
    
    # Draw edges with arrows
    for edge in G.edges():
        node1, node2 = edge
        x1, y1 = pos[node1]
        x2, y2 = pos[node2]
        
        ax.annotate(
            '',
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle='->',
                lw=4,
                color='#C4A7D7',
                alpha=0.6,
                connectionstyle='arc3,rad=0.15'
            ),
            zorder=1
        )
    
    # Draw nodes
    for i, node in enumerate(G.nodes()):
        x, y = pos[node]
        
        if node == center:
            size = 0.22
            color = '#5DBAA4'
        else:
            size = 0.16
            color = pastel_colors[i % len(pastel_colors)]
        
        # Shadow
        shadow = Circle(
            (x - 0.015, y - 0.015), 
            size, 
            facecolor='gray', 
            alpha=0.25,
            zorder=2
        )
        ax.add_patch(shadow)
        
        # Main circle
        circle = Circle(
            (x, y), 
            size, 
            facecolor=color, 
            edgecolor='white', 
            linewidth=5,
            alpha=0.95,
            zorder=3
        )
        ax.add_patch(circle)
        
        # Label
        ax.text(
            x, y, 
            node, 
            fontsize=14 if node == center else 11,
            fontweight='bold',
            ha='center', 
            va='center',
            color='white',
            zorder=4,
            family='sans-serif'
        )
    
    plt.title(
        '🌳 Hierarchical Mind Map', 
        fontsize=28, 
        fontweight='bold', 
        color='#2C2C54', 
        pad=40
    )
    
    ax.axis('off')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    
    output_path = os.path.join('static', 'images', 'mindmap_hierarchical.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(
        output_path, 
        bbox_inches='tight', 
        dpi=200, 
        facecolor='#E8D5F2'
    )
    plt.close()
    
    print(f"✅ Hierarchical mind map created: {output_path}")
    return output_path