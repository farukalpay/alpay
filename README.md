# Symphonic φ Identity Engine

**Author**: Faruk Alpay  

**License**: GPL-3.0  

**Contact**: alpay@lightcap.ai  

**ORCID**: 0009-0009-2207-6528

**PAPER**: https://doi.org/10.5281/zenodo.15398814

---

## 🧠 Overview

This repository implements the **Symphonic φ Identity Engine**, a symbolic, recursive identity generator based on fold dynamics.

It is designed to produce unique, deterministic identity nodes in the format `nXXXXX@alpay.md`, using no randomness, time, hashing, or file persistence. Every fold carries deformation memory, and the system supports fold continuation, resolution, comparison, and public address formatting purely from signal fingerprints.

---

## 📦 Versions

### ✅ `symphonic_phi.py` (v1)

- First release of the φ fold system  
- Core fold + symbolic compression  
- Includes: `--generate`, `--test`, `--iterations`, `--resume`, `--verbose`

### ✅ `symphonic_phi_v2.py`

- Adds support for full **identity resolution** via `--resolve`  
- Supports **waveform-based node parsing** (W-ωC-ηK-κF-f)  
- Prepared for future expansion (e.g., `--graph`, resolver mesh)

### ✅ `symphonic_phi_v3.py` (latest)

- Produces **dual nodes** per fold:
  - ✅ Public node: `nXXXXX@alpay.md`
  - 🔒 Internal node: `nXXXXX|W-...C-...K-...F-...@alpay.md`
- Adds:
  - `--email-only`: Only display public address form
  - `--test-email`: Email validation stats during mass generation
  - `--graph`: Pairwise comparison of φ nodes (ΔID, Δω, Δκ, ΔFold...)
- All modes are file-free and recursive-safe

---

## 🧪 Usage

### 🧬 Generate a public φ identity:

```bash
python3 symphonic_phi_v4.py --generate --email-only
```

### 🧪 Test for uniqueness over 100K folds and check email validity:

```bash
python3 symphonic_phi_v4.py --test --iterations 100000 --email-only --test-email
```

### 🔁 Resume from an internal node (full deformation state):

```bash
python3 symphonic_phi_v4.py --resume "n12345|W-1820C-13K-888F-10@alpay.md" --generate
```

### 🧬 Resolve a node (waveform stats only):

```bash
python3 symphonic_phi_v4.py --resolve "n12345|W-1820C-13K-888F-10@alpay.md"
```

### 📊 Graph pairwise φ node distance:

```bash
python3 symphonic_phi_v4.py --graph   "n23442|W-1820C-13K-888F-123@alpay.md"   "n56888|W-1970C-10K-889F-124@alpay.md"
```

---

## 🔧 Features (v4)

- 🌀 Recursive symbolic τ, ω, δ, ε, η, κ, ζ
- ✉️ Public address mode: `nXXXXX@alpay.md`
- 🔒 Internal wave node: `nXXXXX|W-...@alpay.md`
- 🔁 Resume fold state (`--resume`)
- 🧿 Waveform-based node resolution (`--resolve`)
- 🧮 Drift comparison between nodes (`--graph`)
- 📉 Digit expansion based on pressure
- 📜 Memory embedded in node, no external state
- ✅ RFC-compliant email output (when `--email-only` used)

---

## 🌐 Conceptual Foundations

Built on **Alpay Algebra** and **Frequency Cosmology**, the system treats identity as symbolic deformation:

- Identity is not assigned, but unfolded  
- Every fold is curvature  
- Time is pressure  
- Nodes are resonance anchors

---

## 📜 License

Licensed under [GNU GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html).  
Forking permitted, derivative works must remain open.

---

## 📚 Citation

> Faruk Alpay. *Symphonic φ Identity Engine (v4): Signal-Based Identity, Email Compression & Deformation Memory*. 2024. alpay.md

---

## 🔮 Future Directions

- `--export-graph` → export pairwise comparison as JSON or CSV  
- Web-based φ resolver at `alpay.md`  
- SMTP integration: route `nXXXXX@alpay.md` to resolved ψ profile  
- `φ ↔ GPT` messaging layer using deformational identity

---

> You are not given a name.  
> You are folded into one
> Ξ∞
