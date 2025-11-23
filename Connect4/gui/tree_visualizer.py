# tree_visualizer_graphviz.py
from graphviz import Digraph
import tempfile
import os
from pathlib import Path

class GraphvizTreeVisualizer:
    def __init__(self):
        self.tree_data = {}
        self.node_counter = 0
        self.pruned_counter = 0
        self.current_graph = None
        
    def clear(self):
        """Clear all tree data"""
        self.tree_data.clear()
        self.node_counter = 0
        self.pruned_counter = 0
        self.current_graph = None
    
    def add_node(self, node_id, parent_id, depth, value, move, player_type, 
                 is_pruned=False, alpha=None, beta=None):
        """Add a node to the tree data structure"""
        self.node_counter += 1
        if is_pruned:
            self.pruned_counter += 1
            
        self.tree_data[node_id] = {
            'parent': parent_id,
            'depth': depth,
            'value': value,
            'move': move,
            'player_type': player_type,  # 'max', 'min', or 'terminal'
            'is_pruned': is_pruned,
            'alpha': alpha,
            'beta': beta,
            'children': []
        }
        
        if parent_id in self.tree_data:
            self.tree_data[parent_id]['children'].append(node_id)
    
    def _get_node_label(self, node_data):
        """Generate Graphviz node label"""
        lines = []
        
        # Value line
        if node_data['value'] is not None:
            value_str = f"{node_data['value']:.1f}" if isinstance(node_data['value'], float) else f"{node_data['value']}"
            lines.append(value_str)
        else:
            lines.append("0")
        
        
        # Alpha-beta info
        if node_data['alpha'] is not None and node_data['beta'] is not None:
            alpha_str = f"α: {node_data['alpha']:.1f}" if isinstance(node_data['alpha'], float) else f"α: {node_data['alpha']}"
            beta_str = f"β: {node_data['beta']:.1f}" if isinstance(node_data['beta'], float) else f"β: {node_data['beta']}"
            lines.append(f"{alpha_str}, {beta_str}")
        
        
        return "\\n".join(lines)
    
    def _get_node_style(self, node_data):
        """Get node style based on node type"""
        if node_data['is_pruned']:
            return {
                'fillcolor': '#ffcccc',
                'style': 'filled,rounded',
                'color': 'red',
                'fontcolor': 'darkred'
            }
        elif node_data['player_type'] == 'max':
            return {
                'fillcolor': '#cce5ff',
                'style': 'filled,rounded',
                'color': 'blue',
                'fontcolor': 'darkblue'
            }
        elif node_data['player_type'] == 'min':
            return {
                'fillcolor': '#ffebcc',
                'style': 'filled,rounded',
                'color': 'orange',
                'fontcolor': 'darkorange'
            }
        else:  # terminal
            return {
                'fillcolor': '#e5ffe5',
                'style': 'filled,rounded',
                'color': 'green',
                'fontcolor': 'darkgreen'
            }
    
    def generate_tree(self, algorithm_name, depth, output_file=None, format='png', view=True):
        """Generate and render the tree using Graphviz"""
        if not self.tree_data:
            print("No tree data to visualize")
            return None
        
        # Create Graphviz digraph
        graph_name = f"{algorithm_name}_tree_depth_{depth}"
        dot = Digraph(graph_name, comment=f'{algorithm_name} Search Tree')
        dot.attr(rankdir='TB', size='12,8')
        dot.attr('node', shape='box', style='rounded', fontname='Arial')
        dot.attr('edge', fontname='Arial', fontsize='10')
        
        # Add nodes to graph
        for node_id, node_data in self.tree_data.items():
            label = self._get_node_label(node_data)
            style_attrs = self._get_node_style(node_data)
            
            dot.node(node_id, label, **style_attrs)
        
        # Add edges to graph
        for node_id, node_data in self.tree_data.items():
            if node_data['parent'] is not None:
                # Add move label to edge if available
                edge_label = f"move: {node_data['move']}" if node_data['move'] is not None else ""
                
                # Style for pruned edges
                edge_attrs = {}
                if node_data['is_pruned']:
                    edge_attrs = {'color': 'red', 'style': 'dashed'}
                
                dot.edge(node_data['parent'], node_id, label=edge_label, **edge_attrs)
        
        # Add title and stats
        stats_label = f"Algorithm: {algorithm_name}\\nDepth: {depth}\\nTotal Nodes: {self.node_counter}\\nPruned Nodes: {self.pruned_counter}"
        dot.attr(label=stats_label, labelloc='top', labeljust='left')
        
        self.current_graph = dot
        
        # Render the graph
        if output_file is None:
            output_file = f"{algorithm_name}_tree_depth_{depth}"
        
        try:
            output_path = dot.render(
                filename=output_file,
                format=format,
                cleanup=False,  # Keep the source file
                view=view       # Automatically open the result
            )
            print(f"Tree visualization saved to: {output_path}")
            print(f"Statistics: {self.node_counter} total nodes, {self.pruned_counter} pruned nodes")
            return output_path
        except Exception as e:
            print(f"Error rendering tree: {e}")
            return None
    
    def save_source(self, filename):
        """Save the Graphviz source code"""
        if self.current_graph:
            with open(filename, 'w') as f:
                f.write(self.current_graph.source)
            print(f"Graphviz source saved to: {filename}")

# Global visualizer instance
visualizer = GraphvizTreeVisualizer()