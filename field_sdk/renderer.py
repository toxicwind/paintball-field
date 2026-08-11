#!/usr/bin/env python3
"""Field3DRenderer — Generate professional 3D field visualizations from config JSON.

Usage:
    from field_sdk.renderer import Field3DRenderer
    import json

    with open('config.json') as f:
        config = json.load(f)

    renderer = Field3DRenderer(config)
    renderer.render('output.png', elev=65, azim=-70)

Dependencies: matplotlib, numpy (standard in most Python installs)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patches as mpatches


class Field3DRenderer:
    """Renders 3D field visualizations from config JSON."""

    COLORS = {
        'field_surface': '#4a7c59',
        'field_edge': '#2d5a3d',
        'bunker_inflatable': '#e74c3c',
        'bunker_wooden': '#8b4513',
        'bunker_concrete': '#7f8c8d',
        'bunker_spool': '#3498db',
        'bunker_tube': '#9b59b6',
        'structure_building': '#34495e',
        'objective': '#2ecc71',
        'gateway': '#3498db',
        'ap': '#1abc9c',
        'subzone_castle': 'purple',
        'subzone_helo': 'orange',
        'subzone_urban': 'red',
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

    def _draw_field_surface(self, ax):
        xx, yy = np.meshgrid(np.linspace(0, self.w_m, 20), np.linspace(0, self.h_m, 20))
        zz = np.zeros_like(xx)
        ax.plot_surface(xx, yy, zz, alpha=0.6, color=self.COLORS['field_surface'], shade=True, linewidth=0)
        ax.plot([0, self.w_m, self.w_m, 0, 0], [0, 0, self.h_m, self.h_m, 0], [0, 0, 0, 0, 0], 
               color=self.COLORS['field_edge'], linewidth=3)

    def _draw_box(self, ax, x, y, w, d, h, color):
        verts = [[x-w/2, y-d/2, 0], [x+w/2, y-d/2, 0], [x+w/2, y+d/2, 0], [x-w/2, y+d/2, 0],
                 [x-w/2, y-d/2, h], [x+w/2, y-d/2, h], [x+w/2, y+d/2, h], [x-w/2, y+d/2, h]]
        faces = [[0,1,2,3], [4,5,6,7], [0,1,5,4], [2,3,7,6], [0,3,7,4], [1,2,6,5]]
        for face in faces:
            vf = [verts[i] for i in face]
            ax.add_collection3d(Poly3DCollection([vf], alpha=0.8, facecolor=color, edgecolor='black', linewidth=0.5))

    def _draw_cylinder(self, ax, x, y, r, h, color):
        theta = np.linspace(0, 2*np.pi, 16)
        xc = x + r * np.cos(theta)
        yc = y + r * np.sin(theta)
        ax.plot(xc, yc, np.full_like(theta, h), color=color, linewidth=2)
        ax.plot(xc, yc, np.zeros_like(theta), color=color, linewidth=2)
        for i in range(len(theta)-1):
            verts = [[xc[i], yc[i], 0], [xc[i+1], yc[i+1], 0], [xc[i+1], yc[i+1], h], [xc[i], yc[i], h]]
            ax.add_collection3d(Poly3DCollection([verts], alpha=0.7, facecolor=color, edgecolor='black', linewidth=0.3))

    def _draw_bunkers(self, ax):
        count = self.bunkers.get('count', 30)
        types = self.bunkers.get('types', ['inflatable'])
        density = self.bunkers.get('density', 'medium')
        np.random.seed(hash(self.cfg['field_id']) % 2**32)

        spacing = {'very_high': 6, 'high': 8, 'medium_high': 10, 'medium': 12}.get(density, 15)
        size = {'very_high': 1.5, 'high': 1.8, 'medium_high': 2.0, 'medium': 2.2}.get(density, 2.5)

        positions = []
        margin = 5
        for x in np.arange(margin, self.w_m - margin, spacing):
            for y in np.arange(margin, self.h_m - margin, spacing):
                if len(positions) >= count: break
                jx = x + np.random.uniform(-spacing*0.3, spacing*0.3)
                jy = y + np.random.uniform(-spacing*0.3, spacing*0.3)
                if margin < jx < self.w_m - margin and margin < jy < self.h_m - margin:
                    positions.append((jx, jy))

        for i, (bx, by) in enumerate(positions[:count]):
            btype = types[i % len(types)]
            color = self.COLORS.get(f'bunker_{btype}', '#e74c3c')
            if 'spool' in btype:
                self._draw_cylinder(ax, bx, by, size*0.8, size*1.2, color)
            elif 'tube' in btype:
                self._draw_box(ax, bx, by, size*2, size*0.6, size*0.6, color)
            else:
                self._draw_box(ax, bx, by, size, size*0.8, size*0.6, color)

    def _draw_sub_zones(self, ax):
        for zone_id, zone in self.sub_zones.items():
            loc = zone.get('location', '')
            color = self.COLORS.get(f'subzone_{zone_id}', 'gray')
            if 'northwest' in loc or 'nw' in loc:
                zx, zy = self.w_m * 0.25, self.h_m * 0.75
                zw, zh = self.w_m * 0.4, self.h_m * 0.4
            elif 'center' in loc and 'north' in loc:
                zx, zy = self.w_m * 0.5, self.h_m * 0.8
                zw, zh = self.w_m * 0.3, self.h_m * 0.25
            elif 'south' in loc:
                zx, zy = self.w_m * 0.5, self.h_m * 0.3
                zw, zh = self.w_m * 0.9, self.h_m * 0.5
            else:
                continue
            xx, yy = np.meshgrid(np.linspace(zx - zw/2, zx + zw/2, 10), np.linspace(zy - zh/2, zy + zh/2, 10))
            zz = np.full_like(xx, 0.1)
            ax.plot_surface(xx, yy, zz, alpha=0.15, color=color, shade=False)
            ax.text(zx, zy, 0.5, zone.get('name', zone_id).replace(' ', '\n'), 
                   fontsize=9, color=color, fontweight='bold', ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.5, edgecolor=color))

    def _draw_gateway(self, ax):
        if not self.gw: return
        gx, gy = self.gw.get('x_m', self.w_m/2), self.gw.get('y_m', self.h_m/2)
        self._draw_box(ax, gx, gy, 2, 2, 6, self.COLORS['gateway'])
        ax.plot([gx, gx], [gy, gy], [6, 8], color=self.COLORS['gateway'], linewidth=4)
        ax.text(gx, gy, 9, 'GW', fontsize=11, color='white', fontweight='bold', ha='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='blue', alpha=0.9))

    def _draw_aps(self, ax):
        for ap in self.aps:
            ax_pos = ap.get('x_m', 0), ap.get('y_m', 0)
            self._draw_box(ax, ax_pos[0], ax_pos[1], 1.2, 1.2, 3, self.COLORS['ap'])
            ax.plot([ax_pos[0], ax_pos[0]], [ax_pos[1], ax_pos[1]], [3, 4.5], color=self.COLORS['ap'], linewidth=2)
            ax.text(ax_pos[0], ax_pos[1], 5, ap.get('id', 'AP').split('-')[-1], 
                   fontsize=7, color='white', fontweight='bold', ha='center',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='teal', alpha=0.8))

    def _draw_objectives(self, ax):
        np.random.seed(hash(self.cfg['field_id'] + 'obj') % 2**32)
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
            self._draw_box(ax, ox, oy, 1.5, 1.5, 0.3, self.COLORS['objective'])
            ax.plot([ox, ox], [oy, oy], [0.3, 2], color=self.COLORS['objective'], linewidth=3)
            ax.scatter([ox], [oy], [2.2], color=self.COLORS['objective'], s=80, alpha=0.9)
            ax.text(ox, oy, 3, f'O{i+1}', fontsize=8, color='black', fontweight='bold', ha='center',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='lime', alpha=0.9))

    def render(self, output_path, elev=60, azim=-75, title=None):
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')

        self._draw_field_surface(ax)
        self._draw_bunkers(ax)
        self._draw_sub_zones(ax)
        self._draw_gateway(ax)
        self._draw_aps(ax)
        self._draw_objectives(ax)

        ax.view_init(elev=elev, azim=azim)
        ax.set_xlabel('X (meters)', fontsize=10)
        ax.set_ylabel('Y (meters)', fontsize=10)
        ax.set_zlabel('Height (m)', fontsize=10)

        title_text = title or f"{self.cfg['field_name']} — {self.cfg['dimensions']['area_acres']} acres"
        ax.set_title(title_text, fontsize=14, fontweight='bold', pad=20)

        ax.set_xlim(0, self.w_m)
        ax.set_ylim(0, self.h_m)
        ax.set_zlim(0, max(self.w_m, self.h_m) * 0.4)

        legend_elements = [
            mpatches.Patch(facecolor=self.COLORS['field_surface'], label='Field Surface'),
            mpatches.Patch(facecolor=self.COLORS['bunker_inflatable'], label='Bunkers'),
            mpatches.Patch(facecolor=self.COLORS['gateway'], label='LoRa Gateway'),
            mpatches.Patch(facecolor=self.COLORS['ap'], label='WiFi AP'),
            mpatches.Patch(facecolor=self.COLORS['objective'], label='Objective Node'),
        ]
        if self.sub_zones:
            legend_elements.append(mpatches.Patch(facecolor='purple', alpha=0.3, label='Sub-Zones'))
        ax.legend(handles=legend_elements, loc='upper left', fontsize=9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#1a1a1a')
        plt.close()
        print(f"[RENDERED] {output_path}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python renderer.py <config.json> <output.png> [elev] [azim]")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        config = json.load(f)

    renderer = Field3DRenderer(config)
    elev = float(sys.argv[3]) if len(sys.argv) > 3 else 65
    azim = float(sys.argv[4]) if len(sys.argv) > 4 else -70
    renderer.render(sys.argv[2], elev=elev, azim=azim)
