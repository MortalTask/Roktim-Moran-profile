"""
mosfet_iv_simulator.py

A small, self-contained tool that plots long-channel NMOS I-V characteristics
using the standard square-law MOSFET equations (Sedra/Smith & Sze textbook
models). Built as a public-domain demonstration of device-physics fundamentals
-- no proprietary or lab-specific data is used anywhere in this project.

Author: Roktim Moran
"""

import numpy as np
import matplotlib.pyplot as plt


# ---- Device parameters (typical illustrative values, not measured data) ----
VT0 = 0.7        # Threshold voltage (V)
K_N = 200e-6     # Process transconductance parameter, k'n (A/V^2)
W_L = 10         # Aspect ratio W/L (dimensionless)
LAMBDA = 0.02    # Channel-length modulation coefficient (1/V)


def mosfet_current(vgs, vds, vt=VT0, kn=K_N, w_over_l=W_L, lam=LAMBDA):
    """
    Compute drain current I_D for an NMOS transistor using the square-law
    model, across triode and saturation regions.
    """
    vov = vgs - vt  # overdrive voltage

    if vov <= 0:
        return 0.0  # Cutoff region

    if vds < vov:
        # Triode (linear) region
        i_d = kn * w_over_l * (vov * vds - 0.5 * vds ** 2)
    else:
        # Saturation region, with channel-length modulation
        i_d = 0.5 * kn * w_over_l * vov ** 2 * (1 + lam * vds)

    return i_d


def plot_output_characteristics():
    """I_D vs V_DS for several V_GS values (classic MOSFET output curves)."""
    vds_range = np.linspace(0, 5, 300)
    vgs_values = [1.0, 1.5, 2.0, 2.5, 3.0]

    plt.figure(figsize=(7, 5))
    for vgs in vgs_values:
        id_curve = [mosfet_current(vgs, vds) * 1e3 for vds in vds_range]  # mA
        plt.plot(vds_range, id_curve, label=f"V_GS = {vgs} V")

    plt.title("NMOS Output Characteristics (Square-Law Model)")
    plt.xlabel("V_DS (V)")
    plt.ylabel("I_D (mA)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("output_characteristics.png", dpi=150)
    plt.show()


def plot_transfer_characteristic(vds_fixed=3.0):
    """I_D vs V_GS at a fixed V_DS (transfer curve, used to visualize V_T)."""
    vgs_range = np.linspace(0, 3.5, 300)
    id_curve = [mosfet_current(vgs, vds_fixed) * 1e3 for vgs in vgs_range]  # mA

    plt.figure(figsize=(7, 5))
    plt.plot(vgs_range, id_curve, color="darkorange")
    plt.axvline(VT0, color="gray", linestyle="--", label=f"V_T = {VT0} V")
    plt.title(f"NMOS Transfer Characteristic at V_DS = {vds_fixed} V")
    plt.xlabel("V_GS (V)")
    plt.ylabel("I_D (mA)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("transfer_characteristic.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    plot_output_characteristics()
    plot_transfer_characteristic()
