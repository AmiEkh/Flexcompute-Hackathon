# Flexcompute-Hackathon
Physics-informed inverse design of integrated photonic filters using coupled waveguides. Maps arbitrary target spectra to realizable circuits via transfer-matrix modeling and ML optimization.


# Physics-Informed Design of Optical Filters using Coupled Waveguides

This repository contains a complete pipeline for designing integrated photonic filters using a combination of:
- Waveguide mode simulations  
- Supermode-based coupling extraction  
- Physics-informed compact modeling  
- AI-assisted optimization (PIGNN)  
- Full-wave FDTD validation  

---

## 🚀 Project Overview

We design arbitrary optical filters using cascaded directional couplers. The workflow is structured into three main stages:

1. Waveguide characterization → extract propagation constants (β)  
2. Coupling characterization → extract coupling coefficient (κ) and Ω  
3. Filter design & validation → compact model + AI + FDTD  

---

## 📁 Repository Structure

waveguide_design/  
filter_model_PIGNN/  
fdtd_simulation/  

---

# 1️⃣ Waveguide Design

### Workflow (in order)

### 1. Mode Simulation
Run:
notebooks/waveguide_mode.ipynb

### 2. Width Sweep
Run:
notebooks/width_sweep.ipynb

### 3. Clean Width Sweep Data
Run:
notebooks/width_sweep_data_cleaner.ipynb

### 4. Frequency Sweep
Run:
notebooks/frequency_sweep.ipynb

### 5. Clean Frequency Sweep Data
Run:
notebooks/frequency_sweep_data_cleaner.ipynb

Outputs:
- β_A(λ)
- β_B(λ)

---

# 2️⃣ Coupling Coefficient Extraction (κ, Ω)

### 1. Single Coupling Simulation
notebooks/supermode_coupling.ipynb

### 2. Gap + Frequency Sweep
notebooks/supermode_coupling_gap_frequency_sweeping.ipynb

### 3. Data Cleaning
notebooks/coupling_gap_frequency_sweep.ipynb

Outputs:
- Ω(g, λ)
- κ(g, λ)

---

# 3️⃣ Filter Model + AI (PIGNN)

Folder: filter_model_PIGNN/

### Compact Model
notebooks/filter_compact_model.ipynb

### Interactive Simulator
scripts/filter_live.py

### AI Model
Maps:
Target spectrum → {g_i, L_i}

---

# 4️⃣ FDTD Simulation

Folder: fdtd_simulation/

### Geometry Builder
notebooks/fdtd_geometry_builder.ipynb

### Single Coupling
notebooks/fdtd_single_coupling.ipynb

### Multi Coupling (Example N=4)
notebooks/fdtd_multi_coupling.ipynb

---

# 📊 Data

Each stage contains:
- data/raw/
- data/processed/

---

# ⚠️ Notes

- AI model performance is not fully stable
- Some mismatch between predicted and simulated results
- Model requires further training and debugging

---

# 🧠 Key Idea

Use physics-informed modeling + AI instead of brute-force FDTD.

---

# 🛠 Requirements

pip install -r requirements.txt
