# part 1 - Transpilation
# %% import

import os

from iqm.qiskit_iqm.iqm_provider import IQMProvider
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from rustworkx import spring_layout
from rustworkx.visualization import mpl_draw

from secret import IQM_API_TOKEN

# %% setup backend
os.environ["IQM_TOKEN"] = IQM_API_TOKEN
provider = IQMProvider("https://cocos.resonance.meetiqm.com/garnet")
backend = provider.get_backend()

mpl_draw(
    backend.coupling_map.graph,
    arrows=True,
    with_labels=True,
    node_color="#007f7f",
    pos=spring_layout(backend.coupling_map.graph, num_iter=200),
)

# %% create circuit
num_qb = 3
qc = QuantumCircuit(num_qb)
qc.h(0)
for qb in range(1, num_qb):
    qc.cx(0, qb)

qc.measure_all()
qc.draw("mpl", style="clifford")

shots = 10000
qc_transpiled = transpile(qc, backend=backend)
job = backend.run(qc_transpiled, shots=shots)

res = job.result()
counts = res.get_counts()

plot_histogram(counts)

# %% create GHZ state on different set of qubits
qubits_names_1 = [
    "QB1",
    "QB2",
    "QB5",
]

qubits_names_2 = [
    "QB15",
    "QB19",
    "QB20",
]

# Qiskit identifies qubits with integers, so we need to convert those string by using the IQM Backend method
qubits_1 = [backend.qubit_name_to_index(name) for name in qubits_names_1]
qubits_2 = [backend.qubit_name_to_index(name) for name in qubits_names_2]

# Shows the couplings between the qubits we have selected without showing any of the others.
# Importantly, the first qubit on Qiskit is qubit 0, while the first qubit on Resonance is QB1. So QB1 on Resonance corresponds to qubit 0
#   in Qiskit, and QB5 on Resonance corresponds to QB4 on Qiskit.
reduced_coupling_map_1 = [
    list(edge) for edge in backend.coupling_map if set(edge).issubset(set(qubits_1))
]
print("Reduced coupling map: ", reduced_coupling_map_1)
reduced_coupling_map_2 = [
    list(edge) for edge in backend.coupling_map if set(edge).issubset(set(qubits_2))
]
print("Reduced coupling map: ", reduced_coupling_map_2)

# %% create circuit on qubits_1
qc1 = QuantumCircuit(num_qb)
qc1.h(1)
qc1.cx(1, 0)
qc1.cx(1, 2)
qc1.measure_all()
qc1_transpiled = transpile(
    qc1, backend, coupling_map=reduced_coupling_map_1, optimization_level=3
)
qc1_transpiled.draw("mpl", style="clifford")

# %% create circuit on qubits_2
qc2 = QuantumCircuit(num_qb)
qc2.h(0)
qc2.cx(0, 1)
qc2.cx(0, 2)
qc2.measure_all()
qc2_transpiled = transpile(
    qc2, backend, coupling_map=reduced_coupling_map_2, optimization_level=3
)
qc2_transpiled.draw("mpl", style="clifford")

# %% create circuit on qubits_3 for 9 qubits GHZ
qubits_names_3 = [
    "QB15",
    "QB19",
    "QB20",
    "QB14",
    "QB9",
    "QB4",
    "QB16",
    "QB17",
    "QB12",
]

qubits_3 = [backend.qubit_name_to_index(name) for name in qubits_names_3]
reduced_coupling_map_3 = [
    list(edge) for edge in backend.coupling_map if set(edge).issubset(set(qubits_3))
]
print("Reduced coupling map: ", reduced_coupling_map_3)
qc3 = QuantumCircuit(9)

qc3.h(0)
qc3.cx(0, 1)
qc3.cx(1, 2)
qc3.cx(0, 3)
qc3.cx(3, 4)
qc3.cx(4, 5)
qc3.cx(0, 6)
qc3.cx(6, 7)
qc3.cx(7, 8)
qc3.measure_all()
qc3_transpiled = transpile(
    qc3, backend, coupling_map=reduced_coupling_map_3, optimization_level=3
)
qc3_transpiled.draw("mpl", style="clifford")

# run and plot
# %% qc1
shots = 10000
job1 = backend.run(qc1_transpiled, shots=shots)

res1 = job1.result()
counts1 = res1.get_counts()

plot_histogram(counts1)

# %% qc2
job2 = backend.run(qc2_transpiled, shots=shots)

res2 = job2.result()
counts2 = res2.get_counts()

plot_histogram(counts2)
# %% qc3
job3 = backend.run(qc3_transpiled, shots=shots)

res3 = job3.result()
counts3 = res3.get_counts()

plot_histogram(counts3)
