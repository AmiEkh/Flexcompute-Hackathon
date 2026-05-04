import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from pathlib import Path
from scipy.interpolate import interp1d, RegularGridInterpolator

# ------------------------------------------------------------
# Streamlit config (MUST be first)
# ------------------------------------------------------------

st.set_page_config(layout="wide")

# ------------------------------------------------------------
# Load data (robust path)
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
data_dir = BASE_DIR / "data" / "raw" / "waveguide_data"

beta_file = data_dir / "frequency_sweep_beta_fitted_selected.csv"
omega_file = data_dir / "Omega_gap_wavelength_fitted_selected.csv"

beta_df = pd.read_csv(beta_file)
omega_df = pd.read_csv(omega_file)

# ------------------------------------------------------------
# Select waveguide widths
# ------------------------------------------------------------

width_A_um = 0.4
width_B_um = 0.8

beta_A_df = beta_df[np.isclose(beta_df["width_um"], width_A_um)].copy()
beta_B_df = beta_df[np.isclose(beta_df["width_um"], width_B_um)].copy()

beta_A_df = beta_A_df.sort_values("lambda_um")
beta_B_df = beta_B_df.sort_values("lambda_um")

# ------------------------------------------------------------
# Build beta functions
# ------------------------------------------------------------

beta_A_func = interp1d(
    beta_A_df["lambda_um"],
    beta_A_df["beta_rad_per_um"],
    kind="cubic",
    bounds_error=False,
    fill_value="extrapolate",
)

beta_B_func = interp1d(
    beta_B_df["lambda_um"],
    beta_B_df["beta_rad_per_um"],
    kind="cubic",
    bounds_error=False,
    fill_value="extrapolate",
)

def delta_beta_func(lambda_um):
    return beta_A_func(lambda_um) - beta_B_func(lambda_um)

# ------------------------------------------------------------
# Build Omega(lambda, gap)
# ------------------------------------------------------------

gap_col = "gap_um"
lambda_col = "lambda_um"
omega_col = "Omega_corrected_rad_per_um"

omega_df = omega_df.sort_values([gap_col, lambda_col]).copy()

gap_values = np.sort(omega_df[gap_col].unique())
lambda_values = np.sort(omega_df[lambda_col].unique())

Omega_grid = (
    omega_df.pivot(index=gap_col, columns=lambda_col, values=omega_col)
    .loc[gap_values, lambda_values]
    .to_numpy()
)

Omega_interp = RegularGridInterpolator(
    points=(gap_values, lambda_values),
    values=Omega_grid,
    bounds_error=False,
    fill_value=None,
)

def Omega_func(lambda_um, gap_um):
    lambda_arr = np.asarray(lambda_um, dtype=float)
    gap_arr = np.asarray(gap_um, dtype=float)

    lambda_b, gap_b = np.broadcast_arrays(lambda_arr, gap_arr)

    points = np.column_stack([gap_b.ravel(), lambda_b.ravel()])
    out = Omega_interp(points).reshape(lambda_b.shape)

    return out

# ------------------------------------------------------------
# kappa
# ------------------------------------------------------------

def kappa_func(lambda_um, gap_um):
    Omega = Omega_func(lambda_um, gap_um)
    delta_beta = delta_beta_func(lambda_um)

    inside = Omega**2 - (delta_beta**2) / 4
    inside = np.maximum(inside, 0)

    return np.sqrt(inside)

# ------------------------------------------------------------
# tau
# ------------------------------------------------------------

def tau_func(lambda_um, gap_um, length_um):
    Omega = Omega_func(lambda_um, gap_um)
    kappa = kappa_func(lambda_um, gap_um)

    return (kappa / Omega) * np.sin(Omega * length_um)

# ------------------------------------------------------------
# cascade
# ------------------------------------------------------------

def cascade_transfer(lambda_um, gaps_um, lengths_um):
    A_out = np.ones_like(lambda_um, dtype=complex)

    for g, L in zip(gaps_um, lengths_um):
        A_out *= tau_func(lambda_um, g, L)

    return np.abs(A_out)**2

# ------------------------------------------------------------
# UI Layout
# ------------------------------------------------------------

st.title("Photonic Cascade Filter Designer")

left_col, right_col = st.columns([1, 2.5])

# ------------------------------------------------------------
# LEFT PANEL (sliders)
# ------------------------------------------------------------

with left_col:
    st.header("Design Parameters")

    N = st.slider("Number of stages N", 1, 8, 4)

    st.markdown("### Coupling gaps (µm)")
    gaps_um = []
    for i in range(N):
        g = st.slider(
            f"g_{i+1}",
            0.5, 6.0, 1.0, 0.05,
            key=f"g_{i}"
        )
        gaps_um.append(g)

    st.markdown("### Coupling lengths (µm)")
    lengths_um = []
    for i in range(N):
        L = st.slider(
            f"L_{i+1}",
            0.5, 30.0, 5.0, 0.05,
            key=f"L_{i}"
        )
        lengths_um.append(L)

gaps_um = np.array(gaps_um)
lengths_um = np.array(lengths_um)

# ------------------------------------------------------------
# Compute
# ------------------------------------------------------------

lambda_grid = np.linspace(1.5, 1.6, 800)

T = cascade_transfer(lambda_grid, gaps_um, lengths_um)
T_dB = 10 * np.log10(np.maximum(T, 1e-20))

# ------------------------------------------------------------
# RIGHT PANEL (plot)
# ------------------------------------------------------------

with right_col:
    st.header("Transmission Response")

    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)

    ax.plot(lambda_grid * 1000, T_dB, linewidth=2)

    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Transmission (dB)")
    ax.set_title("Cascade Filter Response")
    ax.grid(True)

    st.pyplot(fig, use_container_width=True)