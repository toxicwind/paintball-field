#!/usr/bin/env python3
"""TopDownRenderer — Generate professional top-down tactical field maps from config JSON.

Like satellite imagery but programmatically generated — always current, no Google Earth needed.
Inspired by military tactical map symbology (MIL-STD-2525) and game minimap rendering.

Usage:
    from field_sdk.topdown import TopDownRenderer
    import json
    with open('config.json') as f:
        config = json.load(f)
    renderer = TopDownRenderer(config)
    renderer.render('topdown.png', title='My Field')
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, RegularPolygon
from datetime import datetime


class TopDownRenderer:
    SYMBOLS = {
        'bunker_inflatable': {'shape': 'roundrect', 'color': '#e74c3c', 'size': 1.8},
        'bunker_wooden': {'shape': 'roundrect', 'color': '#8b4513', 'size': 1.5},
        'bunker_concrete': {'shape': 'square', 'color': '#7f8c8d', 'size': 2.0},
        'bunker_spool': {'shape': 'circle', 'color': '#3498db', 'size': 1.2},
        'bunker_tube': {'shape': 'rect', 'color': '#9b59b6', 'size': (3.0, 0.8)},
        'structure_building': {'shape': 'building', 'color': '#34495e', 'size': (8, 6)},
        'gateway': {'shape': 'tower', 'color': '#3498db', 'size': 2.0},
        'ap': {'shape': 'small_tower', 'color': '#1abc9c', 'size': 1.0},
        'objective': {'shape': 'star', 'color': '#2ecc71', 'size': 1.5},
    }
    
    def __init__(self, config):
        self.cfg = config
        self.w_m = config['dimensions'].get('estimated_length_m', 60)
        self.h_m = config['dimensions'].get('estimated_width_m', 40)
        self.bunkers = config['features']['bunkers']
        self.structures = config['features'].get('structures', [])
        self.sub_zones = config['features'].get('sub_zones', {})
        self.gw = config.get('ghostnet_config', {}).get('gateway_position', {})
        self.aps = config.get('spectreband_config', {}).get('ap_placement', [])
        self.obj_slots = config.get('ghostnet_config', {}).get('objective_slots', 3)
        np.random.seed(hash(config['field_id']) % 2**32)
    
    def _generate_bunker_positions(self):
        count = self.bunkers.get('count', 30)
        types = self.bunkers.get('types', ['inflatable'])
        density = self.bunkers.get('density', 'medium')
        spacing = {'very_high': 6, 'high': 8, 'medium_high': 10, 'medium': 12}.get(density, 15)
        positions = []
        margin = 4
        for x in np.arange(margin, self.w_m - margin, spacing):
            for y in np.arange(margin, self.h_m - margin, spacing):
                if len(positions) >= count: break
                jx = x + np.random.uniform(-spacing*0.3, spacing*0.3)
                jy = y + np.random.uniform(-spacing*0.3, spacing*0.3)
                if margin < jx < self.w_m - margin and margin < jy < self.h_m - margin:
                    btype = types[len(positions) % len(types)]
                    positions.append((jx, jy, btype))
        return positions[:count]
    
    def _draw_symbol(self, ax, x, y, symbol_type, label=None):
        sym = self.SYMBOLS.get(symbol_type, self.SYMBOLS['bunker_inflatable'])
        shape, color, size = sym['shape'], sym['color'], sym['size']
        
        if shape == 'circle':
            patch = Circle((x, y), size, facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.85, zorder=5)
        elif shape == 'roundrect':
            patch = FancyBboxPatch((x - size/2, y - size/2), size, size*0.8,
                                   boxstyle="round,pad=0.1", facecolor=color, edgecolor='black',
                                   linewidth=1.5, alpha=0.85, zorder=5)
        elif shape == 'square':
            patch = patches.Rectangle((x - size/2, y - size/2), size, size,
                                       facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.85, zorder=5)
        elif shape == 'rect':
            w, h = size if isinstance(size, tuple) else (size, size*0.4)
            patch = patches.Rectangle((x - w/2, y - h/2), w, h,
                                       facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.85, zorder=5)
        elif shape == 'building':
            w, h = size if isinstance(size, tuple) else (size, size)
            patch = FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   boxstyle="round,pad=0.2", facecolor=color, edgecolor='black',
                                   linewidth=2, alpha=0.9, zorder=6)
        elif shape == 'tower':
            patch = RegularPolygon((x, y), numVertices=4, radius=size,
                                   facecolor=color, edgecolor='black', linewidth=2, alpha=0.9, zorder=7)
        elif shape == 'small_tower':
            patch = RegularPolygon((x, y), numVertices=3, radius=size,
                                   facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.9, zorder=7)
        elif shape == 'star':
            patch = RegularPolygon((x, y), numVertices=5, radius=size,
                                   facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.95, zorder=8)
        else:
            patch = Circle((x, y), size, facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.85, zorder=5)
        
        ax.add_patch(patch)
        if label:
            ax.text(x, y, label, fontsize=7, color='white', fontweight='bold',
                   ha='center', va='center', zorder=10)
    
    def render(self, output_path, title=None, show_grid=True, show_scale=True, show_legend=True):
        fig, ax = plt.subplots(1, 1, figsize=(16, 12), facecolor='#1a2f1a')
        ax.set_facecolor('#2d5a3d')
        
        # Field boundary
        field_rect = FancyBboxPatch((0, 0), self.w_m, self.h_m,
                                     boxstyle="round,pad=0.5", facecolor='#3a6b4a',
                                     edgecolor='#1a3a2a', linewidth=4, alpha=0.9, zorder=1)
        ax.add_patch(field_rect)
        
        # Sub-zones
        for zone_id, zone in self.sub_zones.items():
            loc = zone.get('location', '')
            if 'northwest' in loc or 'nw' in loc:
                zx, zy, zw, zh = self.w_m * 0.25, self.h_m * 0.75, self.w_m * 0.4, self.h_m * 0.4
                color = 'purple'
            elif 'center' in loc and 'north' in loc:
                zx, zy, zw, zh = self.w_m * 0.5, self.h_m * 0.8, self.w_m * 0.3, self.h_m * 0.25
                color = 'orange'
            elif 'south' in loc:
                zx, zy, zw, zh = self.w_m * 0.5, self.h_m * 0.3, self.w_m * 0.9, self.h_m * 0.5
                color = 'red'
            else:
                continue
            zone_rect = patches.Rectangle((zx - zw/2, zy - zh/2), zw, zh,
                                           facecolor=color, edgecolor=color, linewidth=2,
                                           alpha=0.12, linestyle='--', zorder=2)
            ax.add_patch(zone_rect)
            ax.text(zx, zy + zh/2 + 1, zone.get('name', zone_id), fontsize=10,
                   color=color, fontweight='bold', ha='center', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.5))
        
        # Grid
        if show_grid:
            for x in np.arange(0, self.w_m + 1, 10):
                ax.axvline(x, color='#4a7c59', linewidth=0.5, alpha=0.4, zorder=3)
            for y in np.arange(0, self.h_m + 1, 10):
                ax.axhline(y, color='#4a7c59', linewidth=0.5, alpha=0.4, zorder=3)
            for x in np.arange(0, self.w_m + 1, 20):
                ax.text(x, -1.5, str(int(x)), fontsize=7, color='#7f8c8d', ha='center')
            for y in np.arange(0, self.h_m + 1, 20):
                ax.text(-1.5, y, str(int(y)), fontsize=7, color='#7f8c8d', ha='right', va='center')
        
        # Bunkers
        for bx, by, btype in self._generate_bunker_positions():
            self._draw_symbol(ax, bx, by, f'bunker_{btype}')
        
        # Structures
        for struct in self.structures:
            if 'building' in struct.lower() or 'complex' in struct.lower():
                sx = self.w_m * 0.15 + np.random.uniform(-2, 2)
                sy = self.h_m * 0.15 + np.random.uniform(-2, 2)
                self._draw_symbol(ax, sx, sy, 'structure_building', label='Bldg')
            elif 'keep' in struct.lower() or 'castle' in struct.lower():
                self._draw_symbol(ax, self.w_m * 0.25, self.h_m * 0.75, 'structure_building', label='Keep')
        
        # Gateway
        if self.gw:
            gx, gy = self.gw.get('x_m', self.w_m/2), self.gw.get('y_m', self.h_m/2)
            self._draw_symbol(ax, gx, gy, 'gateway', label='GW')
        
        # APs
        for ap in self.aps:
            ax_pos = ap.get('x_m', 0), ap.get('y_m', 0)
            self._draw_symbol(ax, ax_pos[0], ax_pos[1], 'ap', label=ap.get('id', 'AP').split('-')[-1])
        
        # Objectives
        positions = []
        if self.obj_slots >= 1: positions.append((self.w_m * 0.25, self.h_m * 0.25))
        if self.obj_slots >= 2: positions.append((self.w_m * 0.75, self.h_m * 0.25))
        if self.obj_slots >= 3: positions.append((self.w_m * 0.5, self.h_m * 0.5))
        if self.obj_slots >= 4: positions.append((self.w_m * 0.25, self.h_m * 0.75))
        if self.obj_slots >= 5: positions.append((self.w_m * 0.75, self.h_m * 0.75))
        if self.obj_slots >= 6: positions.append((self.w_m * 0.5, self.h_m * 0.75))
        if self.obj_slots >= 7: positions.append((self.w_m * 0.15, self.h_m * 0.5))
        if self.obj_slots >= 8: positions.append((self.w_m * 0.85, self.h_m * 0.5))
        for i, (ox, oy) in enumerate(positions):
            self._draw_symbol(ax, ox, oy, 'objective', label=f'O{i+1}')
        
        # Scale bar
        if show_scale:
            scale_m = 20 if self.w_m > 80 else 10
            ax.plot([self.w_m - 5 - scale_m, self.w_m - 5], [2, 2], 'w-', linewidth=4, zorder=10)
            ax.text(self.w_m - 5 - scale_m/2, 3.5, f'{scale_m}m', fontsize=10, color='white',
                   fontweight='bold', ha='center', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.7))
        
        # Compass
        ax.annotate('', xy=(self.w_m - 3, self.h_m - 3), xytext=(self.w_m - 3, self.h_m - 8),
                   arrowprops=dict(arrowstyle='->', color='white', lw=2))
        ax.text(self.w_m - 3, self.h_m - 1.5, 'N', fontsize=12, color='white', fontweight='bold', ha='center')
        
        # Legend
        if show_legend:
            legend_elements = [
                patches.Patch(facecolor='#e74c3c', label='Bunkers'),
                patches.Patch(facecolor='#3498db', label='LoRa Gateway'),
                patches.Patch(facecolor='#1abc9c', label='WiFi AP'),
                patches.Patch(facecolor='#2ecc71', label='Objective Node'),
                patches.Patch(facecolor='#34495e', label='Structures'),
            ]
            if self.sub_zones:
                legend_elements.append(patches.Patch(facecolor='purple', alpha=0.3, label='Sub-Zones'))
            ax.legend(handles=legend_elements, loc='upper right', fontsize=9,
                     facecolor='black', edgecolor='white', labelcolor='white')
        
        # Title
        title_text = title or f"{self.cfg['field_name']} — Tactical Map — {self.cfg['dimensions']['area_acres']} acres"
        ax.set_title(title_text, fontsize=14, fontweight='bold', color='white', pad=15)
        
        ax.set_xlim(-3, self.w_m + 3)
        ax.set_ylim(-3, self.h_m + 3)
        ax.set_aspect('equal')
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#1a2f1a')
        plt.close()
        print(f"[RENDERED TOP-DOWN] {output_path}")


if __name__ == '__main__':
    import sys, json
    if len(sys.argv) < 3:
        print("Usage: python topdown.py <config.json> <output.png> [title]")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        config = json.load(f)
    renderer = TopDownRenderer(config)
    renderer.render(sys.argv[2], title=sys.argv[3] if len(sys.argv) > 3 else None)
