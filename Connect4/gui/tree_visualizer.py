"""
Tree Visualizer using Graphviz for Alpha-Beta Pruning and Minimax algorithms.
"""
from graphviz import Digraph
from typing import Optional, Dict, Any


class GraphvizTreeVisualizer:
    """Visualizes game tree search algorithms using Graphviz."""
    
    def __init__(self):
        self.tree_data: Dict[str, Dict[str, Any]] = {}
        self.node_counter = 0
        self.pruned_counter = 0
        self.current_graph: Optional[Digraph] = None
        
    def clear(self) -> None:
        """Clear all tree data and reset counters."""
        self.tree_data.clear()
        self.node_counter = 0
        self.pruned_counter = 0
        self.current_graph = None
    
    def add_node(
        self,
        node_id: str,
        parent_id: Optional[str],
        depth: int,
        value: Optional[float],
        move: Optional[Any],
        player_type: str,
        is_pruned: bool = False,
        alpha: Optional[float] = None,
        beta: Optional[float] = None
    ) -> None:
        """
        Add a node to the tree data structure.
        
        Args:
            node_id: Unique identifier for the node
            parent_id: ID of parent node (None for root)
            depth: Depth level in the tree
            value: Node's evaluation value
            move: Move that led to this node
            player_type: Type of player ('max', 'min', or 'terminal')
            is_pruned: Whether this node was pruned
            alpha: Alpha value at this node
            beta: Beta value at this node
        """
        self.node_counter += 1
        if is_pruned:
            self.pruned_counter += 1
            
        self.tree_data[node_id] = {
            'parent': parent_id,
            'depth': depth,
            'value': value,
            'move': move,
            'player_type': player_type,
            'is_pruned': is_pruned,
            'alpha': alpha,
            'beta': beta,
            'children': []
        }
        
        # Link child to parent
        if parent_id is not None and parent_id in self.tree_data:
            self.tree_data[parent_id]['children'].append(node_id)
    
    def _format_value(self, value: Optional[float]) -> str:
        """Format a numeric value for display."""
        if value is None:
            return "?"
        if isinstance(value, float):
            return f"{value:.1f}"
        return str(value)
    
    def _get_node_label(self, node_data: Dict[str, Any]) -> str:
        """
        Generate a formatted label for a Graphviz node.
        
        Args:
            node_data: Dictionary containing node information
            
        Returns:
            Formatted label string with newlines escaped for Graphviz
        """
        lines = []
        
        # Display node value
        value_str = self._format_value(node_data['value'])
        lines.append(f"Value: {value_str}")
        
        # Display alpha-beta window if available
        if node_data['alpha'] is not None and node_data['beta'] is not None:
            alpha_str = self._format_value(node_data['alpha'])
            beta_str = self._format_value(node_data['beta'])
            lines.append(f"[α={alpha_str}, β={beta_str}]")
        
        return "\\n".join(lines)
    
    def _get_node_style(self, node_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Get visual styling attributes for a node based on its type.
        
        Args:
            node_data: Dictionary containing node information
            
        Returns:
            Dictionary of Graphviz styling attributes
        """
        if node_data['is_pruned']:
            return {
                'fillcolor': '#ffcccc',
                'style': 'filled,rounded',
                'color': 'red',
                'fontcolor': 'darkred',
                'penwidth': '2'
            }
        elif node_data['player_type'] == 'max':
            return {
                'fillcolor': '#cce5ff',
                'style': 'filled,rounded',
                'color': 'blue',
                'fontcolor': 'darkblue',
                'penwidth': '1.5'
            }
        elif node_data['player_type'] == 'min':
            return {
                'fillcolor': '#ffebcc',
                'style': 'filled,rounded',
                'color': 'orange',
                'fontcolor': 'darkorange',
                'penwidth': '1.5'
            }
        else:  # terminal node
            return {
                'fillcolor': '#e5ffe5',
                'style': 'filled,rounded',
                'color': 'green',
                'fontcolor': 'darkgreen',
                'penwidth': '1.5'
            }
    
    def generate_tree(
        self,
        algorithm_name: str,
        depth: int,
        output_file: Optional[str] = None,
        format: str = 'png',
        view: bool = False
    ) -> Optional[str]:
        """
        Generate and render the tree visualization using Graphviz.
        
        Args:
            algorithm_name: Name of the algorithm (e.g., 'Minimax', 'Alpha-Beta')
            depth: Maximum depth of the tree
            output_file: Output filename (without extension)
            format: Output format ('png', 'pdf', 'svg', etc.)
            view: Whether to automatically open the generated file
            
        Returns:
            Path to the generated file, or None if generation failed
        """
        if not self.tree_data:
            print("Warning: No tree data to visualize")
            return None
        
        # Create Graphviz directed graph
        graph_name = f"{algorithm_name}_depth_{depth}".replace(' ', '_')
        dot = Digraph(
            name=graph_name,
            comment=f'{algorithm_name} Search Tree (Depth {depth})'
        )
        
        # Configure graph layout
        dot.attr(rankdir='TB', size='12,8', dpi='300')
        dot.attr('node', shape='box', style='rounded', fontname='Arial', fontsize='10')
        dot.attr('edge', fontname='Arial', fontsize='9', color='gray30')
        
        # Add all nodes to the graph
        for node_id, node_data in self.tree_data.items():
            label = self._get_node_label(node_data)
            style_attrs = self._get_node_style(node_data)
            dot.node(node_id, label, **style_attrs)
        
        # Add all edges to the graph
        for node_id, node_data in self.tree_data.items():
            if node_data['parent'] is not None:
                # Create edge label from move
                edge_label = ""
                if node_data['move'] is not None:
                    edge_label = str(node_data['move'])
                
                # Style pruned edges differently
                edge_attrs = {'label': edge_label}
                if node_data['is_pruned']:
                    edge_attrs.update({
                        'color': 'red',
                        'style': 'dashed',
                        'penwidth': '2'
                    })
                
                dot.edge(node_data['parent'], node_id, **edge_attrs)
        
        # Add summary statistics as graph label
        pruned_pct = (self.pruned_counter / self.node_counter * 100) if self.node_counter > 0 else 0
        stats_label = (
            f"{algorithm_name} Search Tree\\n"
            f"Max Depth: {depth}\\n"
            f"Total Nodes: {self.node_counter}\\n"
            f"Pruned Nodes: {self.pruned_counter} ({pruned_pct:.1f}%)"
        )
        dot.attr(label=stats_label, labelloc='t', labeljust='l', fontsize='12')
        
        self.current_graph = dot
        
        # Determine output filename
        if output_file is None:
            output_file = graph_name
        
        # Render the graph to file
        try:
            output_path = dot.render(
                filename=output_file,
                format=format,
                cleanup=True,  # Remove the intermediate .gv file
                view=view
            )
            print(f"✓ Tree visualization saved to: {output_path}")
            print(f"  Statistics: {self.node_counter} nodes, "
                  f"{self.pruned_counter} pruned ({pruned_pct:.1f}%)")
            return output_path
            
        except Exception as e:
            print(f"✗ Error rendering tree: {e}")
            print(f"  Make sure Graphviz is installed: https://graphviz.org/download/")
            return None
    
    def save_source(self, filename: str) -> None:
        """
        Save the Graphviz source code to a file.
        
        Args:
            filename: Path to save the .gv source file
        """
        if self.current_graph is None:
            print("Warning: No graph has been generated yet")
            return
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.current_graph.source)
            print(f"✓ Graphviz source saved to: {filename}")
        except Exception as e:
            print(f"✗ Error saving source: {e}")


# Global visualizer instance for convenience
visualizer = GraphvizTreeVisualizer()