#!/usr/bin/env python3
"""
SpectreBand Field Calibration Tool

Walks you through calibrating per-AP path loss exponents for your field.
Produces a field config JSON that the server loads for accurate positioning.

Usage:
    python calibrate.py --field blitz_outdoor_50x30 --aps 6 --samples 50
"""

import argparse, json, math, time, sqlite3
import numpy as np
from scipy.optimize import curve_fit

def path_loss_model(d, n, A):
    """RSSI = -10*n*log10(d) + A"""
    return -10 * n * np.log10(d) + A

def calibrate_field(field_name, num_aps, num_samples):
    print(f"=== SpectreBand Field Calibration ===")
    print(f"Field: {field_name}")
    print(f"APs: {num_aps}")
    print(f"Samples per AP: {num_samples}")
    print()

    # Load or create field config
    config_path = f"server/configs/{field_name}.json"
    try:
        with open(config_path) as f:
            config = json.load(f)
    except:
        config = {
            "field_name": field_name,
            "field": {"width": 50, "height": 30},
            "aps": []
        }

    # For each AP, collect samples at known distances
    ap_configs = []

    for ap_idx in range(num_aps):
        ap_id = f"AP-{ap_idx+1:02d}"
        print(f"
--- Calibrating {ap_id} ---")
        print("Place band at known distances from AP and record RSSI.")
        print("Enter 'done' when finished with this AP.")

        distances = []
        rssis = []

        while True:
            d_input = input(f"  Distance from {ap_id} (meters, or 'done'): ").strip()
            if d_input.lower() == 'done':
                break
            try:
                d = float(d_input)
                rssi = int(input(f"  RSSI at {d}m: ").strip())
                distances.append(d)
                rssis.append(rssi)
                print(f"    Recorded: {d}m -> {rssi} dBm")
            except ValueError:
                print("    Invalid input, try again.")

        if len(distances) < 3:
            print(f"  Need at least 3 samples for {ap_id}. Using default n=2.5")
            n, A = 2.5, -45
        else:
            # Fit path loss model
            distances = np.array(distances)
            rssis = np.array(rssis)

            try:
                (n, A), _ = curve_fit(path_loss_model, distances, rssis, p0=[2.5, -45])
                print(f"  Fitted: n={n:.2f}, A={A:.1f} dBm")
            except:
                print(f"  Fit failed, using default n=2.5")
                n, A = 2.5, -45

        # Get AP position
        x = float(input(f"  AP X coordinate (meters): ").strip())
        y = float(input(f"  AP Y coordinate (meters): ").strip())

        ap_configs.append({
            "id": ap_id,
            "x": x,
            "y": y,
            "z": 2.5,
            "tx_power": -30,
            "path_loss": round(n, 2),
            "rssi_at_1m": round(A, 1),
            "channel": [1, 6, 11][ap_idx % 3]
        })

    config["aps"] = ap_configs

    # Calculate expected accuracy
    print(f"
=== Calibration Summary ===")
    for ap in ap_configs:
        print(f"  {ap['id']}: n={ap['path_loss']}, A={ap['rssi_at_1m']} dBm, ({ap['x']},{ap['y']})")

    # Save
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"
Saved to {config_path}")
    print("Restart server to load new calibration.")

def auto_calibrate(field_name, ap_positions):
    """Auto-calibrate using simulation data."""
    print(f"Auto-calibrating {field_name}...")

    config = {
        "field_name": field_name,
        "field": {"width": 50, "height": 30},
        "aps": []
    }

    for i, (x, y) in enumerate(ap_positions):
        ap_id = f"AP-{i+1:02d}"
        # Simulate RSSI samples at various distances
        distances = np.array([1, 2, 3, 5, 8, 10, 15])
        # Outdoor: n=2.5, Indoor concrete: n=3.0, Metal bunkers: n=3.5
        n = 2.8  # Default outdoor with some structures
        A = -45
        rssis = -10 * n * np.log10(distances) + A + np.random.normal(0, 2, len(distances))

        (fitted_n, fitted_A), _ = curve_fit(path_loss_model, distances, rssis, p0=[2.5, -45])

        config["aps"].append({
            "id": ap_id,
            "x": x,
            "y": y,
            "z": 2.5,
            "tx_power": -30,
            "path_loss": round(fitted_n, 2),
            "rssi_at_1m": round(fitted_A, 1),
            "channel": [1, 6, 11][i % 3]
        })

    config_path = f"server/configs/{field_name}.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Auto-calibrated {field_name}, saved to {config_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--field", default="blitz_outdoor_50x30")
    parser.add_argument("--aps", type=int, default=6)
    parser.add_argument("--samples", type=int, default=50)
    parser.add_argument("--auto", action="store_true")
    args = parser.parse_args()

    if args.auto:
        # Blitz field AP positions
        auto_calibrate(args.field, [
            (5, 5), (30, 5), (55, 5),
            (5, 35), (30, 35), (55, 35)
        ])
    else:
        calibrate_field(args.field, args.aps, args.samples)
