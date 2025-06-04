# Universal-Dataset-Encoder
A Generalized Variational Quantum Circuit Framework for Efficient Amplitude-Based Quantum State Preparation

> **Author**: Sejal Sarada  
> **Advisors**: Dr. Debajyoti Bera (IIIT-Delhi), Dr. Kunal Korgaonkar (BITS Pilani Goa Campus)  
> **Thesis Date**: December 2024

---

## 🚀 Overview  
**Revolutionary Quantum State Preparation Framework for the NISQ Era**

This repository presents the **Universal Dataset Encoder (UDE)**, a novel variational quantum circuit (VQC) framework that addresses one of quantum computing’s most critical bottlenecks: efficient and scalable quantum state preparation. Unlike traditional methods that are single-state and dataset-specific, the UDE provides a universal, black-box circuit architecture that can encode **entire dataset matrices into quantum states simultaneously**.

---

## 🎯 Key Innovation

- **Universal Encoding**: A single trainable circuit architecture generalizable to any classical dataset  
- **Multi-State Capability**: Simultaneous preparation of multiple quantum states using ancilla-driven branching  
- **NISQ-Era Optimization**: Low-depth, hardware-friendly design using CRX gates and circular entanglement  
- **Scalable Architecture**: Enables exponential data compression via amplitude encoding strategies

---

## 🔬 Research Contributions

### 1. Hardware-Efficient Circuit Design  
- Shallow-depth VQC with linear scalability  
- Circular entanglement topology using CRX gates  
- O(log n) gate complexity with high expressivity  
- Demonstrated resilience to quantum noise and decoherence  

### 2. Multi-State Quantum Preparation  
- Encodes multiple states using a **single variational circuit**  
- Ancilla qubits used to preserve orthogonality across encoded states  
- Enables batch quantum data encoding for QML  
- Avoids per-state reinitialization and retraining

### 3. Advanced Optimization Framework  
- Fidelity-based cost functions with differentiable quantum circuits  
- Gradient-based optimization using PyTorch autograd  
- Learning rate scheduling and convergence-aware training  
- Supports noisy simulation backends with stability guarantees  

---

## 📊 Experimental Validation

### Single-State Preparation  
- **Perfect Fidelity** (1.0) for 2-qubit and 3-qubit single state encodings  
- Verified on time-series and real-valued vector inputs  
- Rapid convergence under fidelity loss minimization  

### Multi-State Preparation  

| Configuration | # States | Avg. Fidelity | Circuit Depth |
|---------------|----------|----------------|----------------|
| 2-Qubit       | 4        | 0.89           | Shallow        |
| 3-Qubit       | 9        | 0.87           | Moderate       |
| 2-Qubit       | 6        | >0.85          | Minimal        |

---

## 🏗️ Technical Architecture

### Circuit Components  
- **Hadamard Layer**: Initializes equal superposition  
- **Ry Rotations**: Encodes amplitudes without complex phases  
- **CRX-Based Circular Entanglement**: Balances expressivity and connectivity  
- **Ancilla Qubit Control**: Enables conditional state routing in multi-state prep  
- **Symmetric Readout Layer**: Ensures balanced output across branches  

### Mathematical Framework  

**Single-State Objective:**  
Prepare a target state  
\|data⟩ = Σ_j d_j \|j⟩  
Optimize:  
L(θ) = 1 - |⟨data|U(θ)|0⟩|²  

**Multi-State Objective:**  
Prepare G states from dataset {d₁, ..., d_G} using ancilla index g  
Optimize:  
L(θ) = Σ_g α_g(1 - |⟨d_g|VU(θ)|g⟩|²)

---

## 📁 Repository Structure

universal-dataset-encoder/
├── README.md
├── thesis-report/
│ └── EndsemThesisReport.pdf
└── implementations/
├── single_state_preparation.py
└── multi_state_preparation.py

yaml
Copy
Edit

---

## 🎓 Academic Impact

### Research Significance  
This work addresses three major limitations in current literature:  
- High-depth deterministic approaches with poor NISQ performance  
- Limited applicability of single-shot VQC designs  
- Lack of unified frameworks for batch dataset encoding

### Use Cases  
- **Quantum Machine Learning**: Efficient quantum data loaders  
- **Quantum Chemistry**: Compact preparation of multi-electron wavefunctions  
- **QAOA Initialization**: Preparing correlated initial states for optimization  
- **Quantum Simulation**: Complex amplitude distribution synthesis

---

## 🔧 Implementation Details

### Requirements  
- Python ≥ 3.8  
- PyTorch (with autograd)  
- Qiskit or Cirq  
- NumPy, Matplotlib

### Quick Start  

python
# Example: Single-State Encoding
from implementations.single_state_preparation import UniversalEncoder

encoder = UniversalEncoder(n_qubits=3, depth=2)
quantum_state = encoder.encode(classical_data)
fidelity = encoder.evaluate_fidelity(target_state, quantum_state)

---

## 📈 Performance Benchmarks

### Computational Metrics

| Metric              | Value                          |
|---------------------|-------------------------------|
| Circuit Depth       | O(1) to O(poly(n))            |
| Gate Complexity     | Linear in number of qubits    |
| Convergence Time    | Sub-exponential (adaptive)    |
| Memory Footprint    | Optimized for hybrid CPU-QPU  |

### Comparison with Existing Methods

| Method                  | Fidelity   | Circuit Depth | Multi-State Support | NISQ Compatible |
|-------------------------|------------|----------------|----------------------|------------------|
| Grover-Rudolph (2002)   | 1.0        | High           | ❌                   | ❌               |
| Schuld et al. (2020)    | 0.85       | Moderate        | ❌                   | ✅               |
| **UDE (This Work)**     | 0.87–1.0   | Low            | ✅                   | ✅               |

---

## 🔮 Future Research Directions

### Immediate Extensions
- **Hardware Validation**: Deploy the circuit on real quantum devices with noise mitigation techniques  
- **QGAN-Driven Optimization**: Introduce generative adversarial objectives for better generalization  
- **Distribution Encoding**: Extend to full probability distribution mapping rather than vector targets  

### Long-Term Vision
- **Fault-Tolerant Deployment**: Adapt framework for error-corrected quantum architectures  
- **Commercial Solutions**: Develop Dataset-Encoding-as-a-Service (DEaaS) APIs  
- **Hybrid Integration**: Embed the encoder in classical-quantum machine learning pipelines  

---

## 📚 Citation

If you use this work in your research, please cite:

``bibtex
@thesis{sarada2024universal,
  title={Universal Dataset Encoder: A Generalized VQC Approach to Approximate Encoding},
  author={Sarada, Sejal},
  year={2024},
  school={BITS Pilani, Goa Campus},
  supervisor={Bera, Debajyoti and Korgaonkar, Kunal},
  type={Bachelor's Thesis}
}

--

## 👥 Contributors

### Research & Development  
- **Sejal Sarada** — BITS Pilani, Goa Campus

### Supervision  
- **Dr. Debajyoti Bera** — Associate Professor, IIIT Delhi  
- **Dr. Kunal Korgaonkar** — Assistant Professor, BITS Pilani Goa Campus

---

## 📧 Contact

For inquiries or collaboration opportunities:

- **Research inquiries**: Reach out through academic email [sejalsarada13@gmail.com] or institutional channels  
- **Technical issues**: [Open an issue](https://github.com/SejalSarada/universal-dataset-encoder/issues)  
- **Collaborations**: Connect via [LinkedIn]([https://www.linkedin.com/in/sejalsarada/](https://www.linkedin.com/in/sejal-sarada-88ab96204/))

---

> ⚡ **Accelerating Quantum Computing Through Universal State Preparation** ⚡  
> _This work represents a fundamental advancement in quantum state preparation, providing the foundation for more efficient and scalable quantum algorithms in the NISQ era and beyond.
