#!/usr/bin/env python3
"""
Algorithm Comparison Script
Compare Minimax vs Alpha-Beta performance at different depths
"""

from board import Board
from constants import ROWS, COLUMNS
from ai.minimax import minimax_decision
from ai.alphabeta import alphabeta_decision
from ai.stats_tracker import stats
import time


def compare_algorithms(depths=[1, 2, 3, 4, 5]):
    """
    Compare Minimax and Alpha-Beta algorithms at different depths
    """
    print("\n" + "=" * 90)
    print(" " * 25 + "ALGORITHM PERFORMANCE COMPARISON")
    print("=" * 90)
    print(f"\nBoard Size: {ROWS}x{COLUMNS}")
    print(f"Testing Depths (K): {depths}")
    print("\n" + "=" * 90)
    
    results = []
    
    for depth in depths:
        print(f"\n{'':=^90}")
        print(f"{'DEPTH K = ' + str(depth):^90}")
        print(f"{'':=^90}")
        
        # Test Minimax
        print(f"\n{'Minimax Algorithm':^90}")
        print("-" * 90)
        board = Board(ROWS, COLUMNS)
        
        move = minimax_decision(board, depth, visualize=False)
        
        minimax_stats = stats.get_stats()
        minimax_time = minimax_stats['execution_time']
        minimax_nodes = minimax_stats['nodes_expanded']
        minimax_nps = minimax_stats['nodes_per_second']
        
        print(f"  Time Taken:        {minimax_time:>10.4f} seconds")
        print(f"  Nodes Expanded:    {minimax_nodes:>10,} nodes")
        print(f"  Nodes per Second:  {minimax_nps:>10,.0f} nodes/sec")
        print(f"  Best Move:         Column {move}")
        
        results.append({
            'Algorithm': 'Minimax',
            'Depth': depth,
            'Time': minimax_time,
            'Nodes': minimax_nodes,
            'Pruned': 0
        })
        
        # Test Alpha-Beta
        print(f"\n{'Alpha-Beta Algorithm':^90}")
        print("-" * 90)
        board = Board(ROWS, COLUMNS)
        
        move = alphabeta_decision(board, depth, visualize=False)
        
        ab_stats = stats.get_stats()
        ab_time = ab_stats['execution_time']
        ab_nodes = ab_stats['nodes_expanded']
        ab_pruned = ab_stats['nodes_pruned']
        ab_nps = ab_stats['nodes_per_second']
        
        print(f"  Time Taken:        {ab_time:>10.4f} seconds")
        print(f"  Nodes Expanded:    {ab_nodes:>10,} nodes")
        print(f"  Nodes Pruned:      {ab_pruned:>10,} nodes")
        print(f"  Nodes per Second:  {ab_nps:>10,.0f} nodes/sec")
        print(f"  Best Move:         Column {move}")
        
        results.append({
            'Algorithm': 'Alpha-Beta',
            'Depth': depth,
            'Time': ab_time,
            'Nodes': ab_nodes,
            'Pruned': ab_pruned
        })
        
        # Calculate improvement
        print(f"\n{'Performance Comparison':^90}")
        print("-" * 90)
        
        speedup = minimax_time / ab_time if ab_time > 0 else 0
        time_saved = ((minimax_time - ab_time) / minimax_time * 100) if minimax_time > 0 else 0
        node_reduction = ((minimax_nodes - ab_nodes) / minimax_nodes * 100) if minimax_nodes > 0 else 0
        pruning_percentage = (ab_pruned / (ab_nodes + ab_pruned) * 100) if (ab_nodes + ab_pruned) > 0 else 0
        
        print(f"  Speedup Factor:         {speedup:>10.2f}x")
        print(f"  Time Saved:             {time_saved:>10.1f}%")
        print(f"  Node Reduction:         {node_reduction:>10.1f}%")
        print(f"  Pruning Effectiveness:  {pruning_percentage:>10.1f}%")
    
    # Overall Summary
    print("\n" + "=" * 90)
    print(" " * 35 + "OVERALL SUMMARY")
    print("=" * 90)
    
    minimax_results = [r for r in results if r['Algorithm'] == 'Minimax']
    ab_results = [r for r in results if r['Algorithm'] == 'Alpha-Beta']
    
    # Minimax Summary
    print(f"\n{'MINIMAX ALGORITHM':<45} {'ALPHA-BETA ALGORITHM':<45}")
    print("-" * 45 + " " + "-" * 44)
    
    total_minimax_time = sum(r['Time'] for r in minimax_results)
    total_ab_time = sum(r['Time'] for r in ab_results)
    
    avg_minimax_time = total_minimax_time / len(minimax_results)
    avg_ab_time = total_ab_time / len(ab_results)
    
    avg_minimax_nodes = sum(r['Nodes'] for r in minimax_results) / len(minimax_results)
    avg_ab_nodes = sum(r['Nodes'] for r in ab_results) / len(ab_results)
    
    total_pruned = sum(r['Pruned'] for r in ab_results)
    
    print(f"{'Total Time:':<20} {total_minimax_time:>10.4f}s       {'Total Time:':<20} {total_ab_time:>10.4f}s")
    print(f"{'Average Time:':<20} {avg_minimax_time:>10.4f}s       {'Average Time:':<20} {avg_ab_time:>10.4f}s")
    print(f"{'Average Nodes:':<20} {avg_minimax_nodes:>10,.0f}        {'Average Nodes:':<20} {avg_ab_nodes:>10,.0f}")
    print(f"{'Total Nodes:':<20} {sum(r['Nodes'] for r in minimax_results):>10,}        {'Total Pruned:':<20} {total_pruned:>10,}")
    
    # Overall Performance
    print("\n" + "-" * 90)
    print(f"{'OVERALL PERFORMANCE IMPROVEMENT (Alpha-Beta vs Minimax)':^90}")
    print("-" * 90)
    
    overall_speedup = total_minimax_time / total_ab_time if total_ab_time > 0 else 0
    overall_node_reduction = ((avg_minimax_nodes - avg_ab_nodes) / avg_minimax_nodes * 100) if avg_minimax_nodes > 0 else 0
    
    print(f"  Average Speedup:        {overall_speedup:>8.2f}x faster")
    print(f"  Average Node Reduction: {overall_node_reduction:>8.1f}% fewer nodes explored")
    print(f"  Total Time Saved:       {total_minimax_time - total_ab_time:>8.4f} seconds")
    
    print("\n" + "=" * 90)
    
    # Detailed Table
    print(f"\n{'DETAILED RESULTS TABLE':^90}")
    print("=" * 90)
    print(f"{'Algorithm':<12} {'Depth':<8} {'Time (s)':<12} {'Nodes':<12} {'Pruned':<12} {'Speedup':<10}")
    print("-" * 90)
    
    for i in range(len(depths)):
        minimax_result = minimax_results[i]
        ab_result = ab_results[i]
        speedup = minimax_result['Time'] / ab_result['Time'] if ab_result['Time'] > 0 else 0
        
        print(f"{'Minimax':<12} {minimax_result['Depth']:<8} {minimax_result['Time']:<12.4f} {minimax_result['Nodes']:<12,} {'-':<12} {'-':<10}")
        print(f"{'Alpha-Beta':<12} {ab_result['Depth']:<8} {ab_result['Time']:<12.4f} {ab_result['Nodes']:<12,} {ab_result['Pruned']:<12,} {speedup:<10.2f}x")
        print()
    
    print("=" * 90)
    print("\nComparison complete!")
    
    return results


if __name__ == "__main__":
    print("\nStarting Algorithm Comparison...")
    print("This will compare Minimax and Alpha-Beta at various depths.\n")
    
    # Get depths from user or use default
    try:
        user_input = input("Enter depths to test (comma-separated, e.g., '1,2,3,4,5') or press Enter for default [1,2,3,4,5]: ").strip()
        if user_input:
            depths = [int(d.strip()) for d in user_input.split(',')]
        else:
            depths = [1, 2, 3, 4, 5]
        
        print(f"\nTesting depths: {depths}")
        time.sleep(1)
        
        results = compare_algorithms(depths)
        
    except KeyboardInterrupt:
        print("\n\nComparison cancelled by user.")
    except Exception as e:
        print(f"\n\nError: {e}")