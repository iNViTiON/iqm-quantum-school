# Quantum School: Day 1 - https://colab.research.google.com/drive/1gycBa4T-RHfBBJlu6XBICR3SWIoA9BpD

# %% import
from qrisp import QuantumArray, QuantumModulus, QuantumVariable, cx, h, t, x, z
from qrisp.interface import IQMBackend

from secret import IQM_API_TOKEN

# %% Task 2
# %% Task 2.1: Run the code below that creates qubit states |0⟩, |1⟩, |+⟩ and |−⟩ using qrisp.
# Describe what results you get when measuring each state.

# TODO: create single-qubit variables
zero = QuantumVariable(1)
one = QuantumVariable(1)
plus = QuantumVariable(1)
minus = QuantumVariable(1)

# TODO: apply gates to change the state of the qubits
x(one)

h(plus)

h(minus)
z(minus)

print("|0>:")
print(zero.qs.statevector())  # pyright: ignore[reportOptionalMemberAccess]
# Printing a QuantumVariable outputs the probability of measuring the qubit to be in each basis state.
print(zero)

print("|1>:")
print(one.qs.statevector())  # pyright: ignore[reportOptionalMemberAccess]
print(one)

print("|+>:")
print(plus.qs.statevector())  # pyright: ignore[reportOptionalMemberAccess]
print(plus)

print("|->:")
print(minus.qs.statevector())  # pyright: ignore[reportOptionalMemberAccess]
print(minus)

# %% Task 2.2 (Homework): Let's try something more complex. Create the state sqrt(2)*(|0> + exp(3*I*pi/4)*|1>)/2 ( ≈0.71|0⟩+(−0.5+0.5i)|1⟩ ) using x, h, t, z, y or s gates.
qubit = QuantumVariable(1)

# TODO: Apply gates to prepare the specified state
h(qubit)
t(qubit)
t(qubit)
t(qubit)

print(qubit.qs.statevector())  # pyright: ignore[reportOptionalMemberAccess]
print(qubit)

print(str(qubit.qs.statevector()) == "sqrt(2)*(|0> + exp(3*I*pi/4)*|1>)/2")  # pyright: ignore[reportOptionalMemberAccess]

# %% Task 3
# %% Task 3.1: Modify the code below to evaluate some of the QuantumVariables you created in Task 2.1 on IQM's quantum hardware (zero, one, plus, minus).
quantum_computer = IQMBackend(api_token=IQM_API_TOKEN, device_instance="garnet")
# %% Task 3.1-2
# The qv.get_measurement() function behaves just like print(qv), but we'll need to use get_measurement() to run on a real quantum computer.
zero.get_measurement(backend=quantum_computer, shots=10000)
plus.get_measurement(backend=quantum_computer, shots=10000)
one.get_measurement(backend=quantum_computer, shots=10000)
minus.get_measurement(backend=quantum_computer, shots=10000)

# %% Task 4
# %% Task 4.1: Execute the following code in your environment. It will create a Bell state and simulate it on the qrisp simulator.
qv = QuantumVariable(2)
h(qv[0])
cx(qv[0], qv[1])
# The qv.get_measurement() function behaves just like print(qv), but we'll need to use get_measurement() to run on a real quantum computer.
qv.get_measurement()
# %% Task 4.1-2
# Let's also take a look at the underlying circuit that was created. In qrisp this is done by accessing the qs attribute of the QuantumVariable.
print(qv.qs)

# %% Task 4.2: Modify the code above to create a GHZ state with 3 qubits instead of a Bell state with 2 qubits. Simulate the modified circuit on the qrisp simulator.
qv = QuantumVariable(3)
h(qv[0])
cx(qv[0], qv[1])
cx(qv[1], qv[2])
qv.get_measurement()
# %% Task 4.2-2
print(qv.qs)
# %% Task 4.2-3
# Simulating a GHZ state on the qrisp simulator is great, but you know what is even better? Running it on real quantum hardware!
# Now update the below code to run the circuit on IQM Resonance hardware. You will need to provide your API key (available in your IQM Resonance account drawer). Also, make sure to check the website to verify that the device you are choosing is currently online.
qv.get_measurement(backend=quantum_computer, shots=10000)
# %% Task 4.3
# Repeat the above experiment, but this time create a GHZ state with at least 10 qubits. How does the result on the quantum hardware compare to the simulated results? Why?
qv = QuantumVariable(10)
h(qv[0])
cx(qv[0], qv[1])
cx(qv[1], qv[2])
cx(qv[2], qv[3])
cx(qv[3], qv[4])
cx(qv[4], qv[5])
cx(qv[5], qv[6])
cx(qv[6], qv[7])
cx(qv[7], qv[8])
cx(qv[8], qv[9])
qv.get_measurement()
# %% Task 4.3-2
print(qv.qs)
# %% Task 4.3-3
qv.get_measurement(backend=quantum_computer, shots=10000)
# %% Task 4 (again? The previous task were with subtask 3.x, while having Task 3 with subtask 3.x; and this one is Task 4 with subtask 4.x)
# %% Task 4.1: Adapt the GHZ circuit to reflect the connectivity given by the device. You can check the connectivity for any given device on IQM Resonance.
# I skip 4.1 & 4.2
#
#
# %% Outlook: More qrispy content
# Qrisp offers plenty more of in-built functionality. More data types (hello QuantumFloat, QuantumModulus, ...), arithmetic operations, built-in algorithm primitives (more on this at a later stage).
# For now, let's see some other data types available in qrisp! One that is used, for example, in Shor's algorithm is the Quantum Modulus type. It represents elements of a residue class ring, that is, integers modulo  n .
# %% Task 4.3: Run the adapted GHZ circuit on IQM Resonance hardware.
qm = QuantumModulus(3)  # represent elements of Z/ 3Z
qm[:] = 2
print(qm)
# %%
qm2 = qm + qm  # addition in Z/3Z
print(qm2)
# %%
h(qm[1])
# %%
print(qm)
# %% Quantum Arrays
# %% Task 4.4: fill in the code below to use the QuantumArray data type to create a GHZ state with 10 qubits and run it on a real quantum computer.
qa = QuantumArray(
    qtype=QuantumVariable(1), shape=10
)  # Creates a Quantum Array of 10 qubits


def GHZ(qv):
    # TODO: implement GHZ state preparation
    h(qv[0])
    cx(qv[0], qv[1])
    cx(qv[1], qv[2])
    cx(qv[2], qv[3])
    cx(qv[3], qv[4])
    cx(qv[4], qv[5])
    cx(qv[5], qv[6])
    cx(qv[6], qv[7])
    cx(qv[7], qv[8])
    cx(qv[8], qv[9])
    pass


GHZ(qa)

print(qa)
print(qa.qs)
# %%
print(qa.get_measurement(backend=quantum_computer))
