# %% import
from IPython.display import display, HTML
from iqm.iqm_client import Circuit
from iqm.pulla.pulla import Pulla
from iqm.pulse.playlist.visualisation.base import inspect_playlist
from iqm.qiskit_iqm.iqm_provider import IQMProvider
from iqm.qiskit_iqm.qiskit_to_iqm import serialize_instructions
from qrisp import QuantumCircuit

from secret import IQM_API_TOKEN

# %%
p = Pulla(
    "https://resonance.meetiqm.com/garnet", token=IQM_API_TOKEN
)

compiler = p.get_standard_compiler()

# %% GHZ state
qc_0 = QuantumCircuit(3)
qc_0.h(0)
qc_0.cx(0,1)
qc_0.cx(0,2)
qc_0.measure([0,1,2])

print(qc_0)

# %% transpile
provider = IQMProvider('https://resonance.meetiqm.com/garnet', token=IQM_API_TOKEN)
backend = provider.get_backend()

transpiled_qc = qc_0.transpile(backend=backend)
print(transpiled_qc)
# %% transqile to qiskit
qiskit_circuit = transpiled_qc.to_qiskit()
# %% compilation
iqm_instructions = serialize_instructions(qiskit_circuit, {i : "QB" + str(i+1) for i in range(qiskit_circuit.num_qubits)})
iqm_circuit = Circuit(name = "my_circuit", instructions = iqm_instructions)

playlist, context = compiler.compile([iqm_circuit])
# %% visualize playlist
display(HTML(inspect_playlist(playlist)))
# export playlist to file, since ZED REPL doesn't support display yet
html_content = inspect_playlist(playlist)
with open("day3-2_playlist.html", "w") as file:
    file.write(html_content)
