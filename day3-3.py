# %% import
import matplotlib.pyplot as plt
import numpy as np
from iqm.pulla.pulla import Pulla
from iqm.pulse.builder import CircuitOperation as Op
from iqm.pulse.circuit_operations import Circuit

from secret import IQM_API_TOKEN

# %% 1. Preparation - Connecting to the QPU station control
p = Pulla(
    "https://resonance.meetiqm.com/garnet", token=IQM_API_TOKEN
)

compiler = p.get_standard_compiler()

# %% 2. Measurement operation
# Qubit readout in superconducting systems is done via **superconducting resonators** (e.g. LC oscillators) that are coupled to the transmon qubits in the QPU. The coupling between the qubit and the resonator can be described with the [Jaynes-Cummings model](https://en.wikipedia.org/wiki/Jaynes%E2%80%93Cummings_model), which allows for two different regimes of the system, the **resonant** and the **dispersive** one. In the latter, looking at the spectrum of the resonator, one can infer the state of the qubit thanks to the **shift** in the resonator's frequency caused by the coupling.
# The raw measurement signal is typically represented as a **complex number** as function of time. The measurement instrument integrates the signal over time to yield a complex number, one per measurement operation.
# What we are used to see as a result of a measurement looks different though, right? An extra step is required: the complex number is rotated so that the difference between the states is maximal along the real axis. The real value of the signal is then compared with a **calibrated threshold value**, from which we get the well known 0/1 labels :)
# In the following, **we will not perform the thresholding** to investigate and get familiar with the raw results of a measurement operation!
# ### 2.1 Measuring a qubit in different states
# Knowing now that the readout signal depends on the state of the qubit, our strategy will be to prepare the qubits in different states and compare observations!
# We will inspect the results of 3 circuits:
# 1. Prepare a qubit in the $|0\rangle$ state and measure.
# 2. Prepare a qubit in the $|1\rangle$ state and measure.
# 3. Prepare a qubit in the superposition of $|0\rangle$ and $|1\rangle$ and measure.
# Below we use the IQM Pulse syntax to define the circuits (you can find the documentation [here](https://docs.meetiqm.com/iqm-pulse/)).
# The PRX gate is defined as $R_{\phi}(\theta) = e^{-i(X cos(\phi)+Y sin(\phi))\frac{\theta}{2}}$. We can prepare the qubit in the three different states above changing the rotation angle $\theta$ and setting the phase angle $\phi$ to zero.

qubit = "QB1"
circuits = []
for name, angle in zip(["state0", "state1", "superposition"], [0.0,np.pi,np.pi/2]):
    circuit = Circuit(name, [
        Op("prx", (qubit,), args={"angle": angle, "phase": 0.0}),
        Op("measure", (qubit,), args={"key": "M"})
    ])
    circuits.append(circuit)

# %% To see the unthresholded signals, we need to tweak the **calibration settings** of the `measure` operation.
# The `measure` operation can be implemented in more than one way. To see the available settings of all implementations, you can use `print_implementations_trees` (the first one in the list is the default).
compiler.print_implementations_trees(compiler.builder.op_table["measure"])

# %% We need to change the `acquisition_type` of the `constant` implementation from `threshold` to `complex`.
# IQM Crystal way
compiler.amend_calibration_for_gate_implementation("measure_fidelity", "constant", (qubit, ), {"acquisition_type": "complex"})

# IQM Star way
# updated_cal_set = compiler.get_calibration()
# for q in ["QB1", "QB2", "QB3", "QB4", "QB5", "QB8", "QB9", "QB10", "QB11", "QB13", "QB15", "QB16", "QB17", "QB19", "QB20", "QB21"]:
#     updated_cal_set[f'gates.measure_fidelity.constant.{q}.acquisition_type'] = 'complex'
# compiler.set_calibration(updated_cal_set)

# %% Now we can execute the circuits with the modified settings:
playlist, context = compiler.compile(circuits)
settings, context = compiler.build_settings(context, shots=1000)
job = p.submit_playlist(playlist, settings, context=context)
job.wait_for_completion()
qiskit_result = sweep_job_to_qiskit(job, shots=shots, execution_options=context['options'])

print(f"Qiskit result counts:\n{qiskit_result.get_counts()}\n")

# %% Analyze the results

state_0_results = np.array(job.result[0]["M"]).squeeze()
state_1_results = np.array(job.result[1]["M"]).squeeze()
state_2_results = np.array(job.result[2]["M"]).squeeze()
plt.figure()
plt.scatter(np.real(state_0_results), np.imag(state_0_results), label="|0>", s=4)
plt.scatter(np.real(state_1_results), np.imag(state_1_results), label="|1>", s=4)
plt.scatter(
    np.real(state_2_results), np.imag(state_2_results), label="Superposition", s=4
)
plt.xlabel("Re")
plt.ylabel("Im")
plt.gca().set_aspect("equal")
plt.grid()
plt.legend()
