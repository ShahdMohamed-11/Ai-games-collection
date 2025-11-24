import graphviz
import threading
import time
from pathlib import Path


class TreeNode:
    def __init__(self, col, score, depth, is_maximizing, alpha, beta):
        self.col = col
        self.score = score
        self.depth = depth
        self.is_maximizing = is_maximizing
        self.alpha = alpha
        self.beta = beta
        self.children = []
        self.parent = None
        self.pruned = False
        self.id = None  # Unique identifier for graphviz
        self.is_chance = False  # For expected minimax chance nodes
        self.probability = None  # For expected minimax probabilities
    
    def add_child(self, child):
        child.parent = self
        self.children.append(child)


class TreeVisualizer:
    def __init__(self):
        self.root = None
        self.node_counter = 0
        self.output_dir = Path("tree_visualizations")
        self.output_dir.mkdir(exist_ok=True)
        self.current_file = None
        self.update_pending = False
        self.render_thread = None
        
    def generate_node_id(self):
        """Generate unique node ID"""
        self.node_counter += 1
        return f"node_{self.node_counter}"
    
    def assign_ids(self, node):
        """Recursively assign IDs to all nodes"""
        if node.id is None:
            node.id = self.generate_node_id()
        for child in node.children:
            self.assign_ids(child)
    
    def create_graph(self):
        """Create graphviz graph from tree structure"""
        if self.root is None:
            return None
        
        # Create directed graph
        dot = graphviz.Digraph(comment='Minimax Tree')
        dot.attr(rankdir='TB')  # Top to Bottom
        dot.attr('node', fontname='Arial', fontsize='12')
        dot.attr('edge', fontname='Arial', fontsize='10')
        
        # Assign IDs to nodes
        self.node_counter = 0
        self.assign_ids(self.root)
        
        # Add nodes and edges
        self._add_nodes_and_edges(dot, self.root)
        
        return dot
    
    def _add_nodes_and_edges(self, dot, node):
        """Recursively add nodes and edges to graph"""
        
        # Determine node shape and color based on type
        if node.is_chance:
            # Chance nodes (diamond shape)
            shape = 'diamond'
            fillcolor = 'lightyellow'
            fontcolor = 'black'
        elif node.pruned:
            # Pruned nodes
            shape = 'circle'
            fillcolor = 'lightgray'
            fontcolor = 'black'
        elif node.is_maximizing is None:
            # Root or terminal nodes
            shape = 'circle'
            fillcolor = 'white'
            fontcolor = 'black'
        elif node.is_maximizing:
            # Maximizing nodes
            shape = 'circle'
            fillcolor = 'lightblue'
            fontcolor = 'black'
        else:
            # Minimizing nodes
            shape = 'circle'
            fillcolor = 'lightcoral'
            fontcolor = 'black'
        
        # Format node label - handle None scores properly
        if node.score is None:
            score_text = "..."
        elif isinstance(node.score, (int, float)):
            if isinstance(node.score, float):
                score_text = f"{node.score:.2f}"
            else:
                score_text = str(node.score)
        else:
            score_text = str(node.score)
        
        if node.is_chance:
            # Chance node label (simpler)
            label = f"{node.col}\n{score_text}"
        elif node.alpha is not None and node.beta is not None:
            # Alpha-beta node label
            alpha_str = f"{node.alpha:.1f}" if node.alpha != float('-inf') else "-∞"
            beta_str = f"{node.beta:.1f}" if node.beta != float('inf') else "∞"
            label = f"{score_text}\n────\nα:{alpha_str}\nβ:{beta_str}"
        else:
            # Simple node label (for minimax without alpha-beta)
            label = score_text
        
        # Add node with appropriate styling
        dot.node(node.id, label=label, 
                shape=shape,
                style='filled', 
                fillcolor=fillcolor, 
                fontcolor=fontcolor,
                width='1.2' if shape == 'circle' else '1.4',
                height='1.2' if shape == 'circle' else '1.0',
                fixedsize='true')
        
        # Add edges to children
        for child in node.children:
            edge_color = 'gray' if child.pruned else 'black'
            edge_style = 'dashed' if child.pruned else 'solid'
            
            # Add probability label if it exists
            if hasattr(child, 'probability') and child.probability is not None:
                edge_label = f"p={child.probability:.2f}"
                dot.edge(node.id, child.id, label=edge_label, 
                        color=edge_color, style=edge_style)
            else:
                dot.edge(node.id, child.id, color=edge_color, style=edge_style)
            
            self._add_nodes_and_edges(dot, child)
    
    def render_tree(self):
        """Render the tree to a file and open it"""
        if self.root is None:
            return
        
        try:
            dot = self.create_graph()
            if dot is None:
                return
            
            # Generate filename with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"minimax_tree_{timestamp}"
            filepath = self.output_dir / filename
            
            # Render to PNG and PDF
            dot.render(filepath, format='png', view=True, cleanup=True)
            
            self.current_file = str(filepath) + '.png'
            print(f"Tree visualization saved to: {self.current_file}")
            
        except Exception as e:
            print(f"Error rendering tree: {e}")
    
    def update_display(self):
        """Queue an update to render the tree"""
        self.update_pending = True
    
    def start_render_loop(self):
        """Start background thread to render updates"""
        def render_loop():
            while True:
                if self.update_pending:
                    self.update_pending = False
                    self.render_tree()
                time.sleep(0.5)  # Check every 0.5 seconds
        
        if self.render_thread is None or not self.render_thread.is_alive():
            self.render_thread = threading.Thread(target=render_loop, daemon=True)
            self.render_thread.start()


# Global instance
visualizer = TreeVisualizer()


def start_visualization():
    """Start the visualization renderer"""
    visualizer.start_render_loop()
    print("\n" + "="*60)
    print("Minimax Tree Visualization Started")
    print("="*60)
    print("Tree visualizations will be saved to: tree_visualizations/")
    print("A new window will open automatically showing the tree.")
    print("Legend:")
    print("  🔵 Blue circles = Maximizing (AI)")
    print("  🔴 Red circles = Minimizing (Human)")
    print("  🟡 Yellow diamonds = Chance nodes (Expected Minimax)")
    print("  ⚫ Gray circles = Pruned branches")
    print("="*60 + "\n")