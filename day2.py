# %% import
import networkx as nx
import numpy as np
from dimod import Binary, ConstrainedQuadraticModel, quicksum
from iqm.applications.maxcut import maxcut_generator
from iqm.applications.qubo import ConstrainedQuadraticInstance
from iqm.qaoa.backends import SamplerResonance, SamplerSimulation
from iqm.qaoa.qubo_qaoa import QUBOQAOA
from qrisp import QuantumFloat, QuantumVariable, cx, h, x
from qrisp.grover import grovers_alg, tag_state
from qrisp.interface import IQMBackend
from toolz import pipe

from secret import IQM_API_TOKEN

# %% Part 1: Bernstein-Vazirani algorithm
# Step 1: Initialize a quantum variable
length_of_secret_code = 4
inputs = QuantumVariable(
    length_of_secret_code
)  # TODO: create the input quantum variables

# Step 2: Apply Hadamard gates to all qubits
h(inputs)


# %% oracle implementation
def oracle(qubits, secret_code):
    # TODO
    answerQubit = QuantumVariable(1)
    x(answerQubit)
    h(answerQubit)
    for i in range(length_of_secret_code):
        if secret_code[i] == "1":
            cx(qubits[i], answerQubit)
    return qubits


# Step 3: Define a secret code and call the oracle
secret_code = "1011"
oracle(inputs, secret_code)
# TODO

# Step 4: Apply a final round of Hadamard gates
h(inputs)

# TODO

# Simulate the circuit
print(inputs)

# If you want to see the circuit you have built so far, you can print it out using the print function:
print(inputs.qs)

# %% Now, use the IQM backend to execute the circuit and measure the qubits to retrieve the secret code.
quantum_computer = IQMBackend(api_token=IQM_API_TOKEN, device_instance="garnet")
# %%
inputs.get_measurement(backend=quantum_computer)

# %% Part 2: Variational Quantum Algorithms: QAOA and MaxCut
# In this section, you will...
# ...solve the MaxCut problem with QAOA by using the iqm.qaoa package to use QAOA.
# ...experiment with the built-in functions of iqm.qaoa.
# Recall that the MaxCut problem is the following:

# Suppose that you have  N  students who are taking an exam. You must assign each student to take the exam in one of two rooms, which we will call room  0  and room  1 . Students who are friends and in the same room are more likely to cheat. Your goal is to minimize the chance of cheating by separating as many pairs of friends as possible. Assume you know the friendships.

# Setting up the problem
# We start by assigning each student a variable  xi  which is equal to  0  if they are assigned to room  0  and  1  if they are in room  1 .

# The cost function encodes the friendships. In lecture, we wrote it as
# H({Zi})=∑i<jJijZiZj
# where  Jij  is 1 if students  i  and  j  are friends and 0 if not, and  Zi  is  −1  if student  i  is assigned to room  0  and  Zi  is  +1  if student  i  is assigned to room  1 .

# Unfortunately, the software requires us to write this in terms of  xi , which can be 0 or 1, instead of  Zi . A little straightforward math shows us that  Zi=1−2xi , which means that we can rewrite the cost function as
# H({xi})=∑i<jJij(1−2xi)(1−2xj)
num_students = 6
# Alice, Bob, Charlie, David, Eve, Frank
Jij = [
    [0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
]
# TO DO: Fill in the question marks
# We set everything in the bottom left to 0 to avoid double-counting every friendship, although this won't have an effect in the end

# Next we need to create the object representing the MaxCut problem and the cost function. This is done using the dimod module, which has handy tools for creating functions of binary variables.

# %% Task: Implement the cost function in the code below.
# Create the variables. This is just a list of variables where x[i] represents the variable xi.
xi = {i: Binary(i) for i in range(num_students)}

# Define the cost function. As written here, quicksum implements the sum over i and j.
cost = quicksum(
    # TODO: Implement the cost function
    Jij[i][j] * (1 - 2 * xi[i]) * (1 - 2 * xi[j])
    for i in range(num_students)
    for j in range(num_students)
)
# Create a problem which can be passed into the QAOA algorithm
MaxCut_QUBO = ConstrainedQuadraticModel()

# Set the cost function of the problem
MaxCut_QUBO.set_objective(cost)

# Now create the problem
MaxCut_instance = ConstrainedQuadraticInstance(MaxCut_QUBO)

# %% Connecting to Resonance
# It turns out that for special classes of problems, including this one, there are efficient classical ways to optimize the ansatz. Why, then, do we need the quantum computer at all? The thing that is still difficult classically is to take the state with its optimized parameters and find the probabilities of getting all of the possible output measurements. Ideally, the most probable output is the correct answer.
# To do this, we're going to connect to Resonance.
# This will look a little different from what we've done before in order to work with the QAOA interface. We'll then set up a SamplerResonance object, which tells the QAOA algorithm to use the quantum computer to find the probabilities of all the outputs.

iqm_url = "https://cocos.resonance.meetiqm.com/garnet"
# sampler = SamplerResonance(
#     token=IQM_API_TOKEN, server_url=iqm_url, transpiler="Default"
# )
sampler = SamplerSimulation()

# %% Running QAOA
# We now create the QUBO QAOA instance from the problem instance and train it (run the optimization loop to find find optimal variational parameters).

# The train method has several possible parameters. By default, it uses uses analytical formulas if the QAOA has one layer and a simulator otherwise.

# Recall that the  i th layer of the QAOA ansatz applies the circuit
# e−iβiHmixe−iγiHc
# to the qubits, where the variational parameters are  βi  and  γi . So, the number of variational parameters in QAOA is twice the number of layers.
MaxCut_qaoa = QUBOQAOA(
    problem=MaxCut_instance,
    num_layers=1,  # TODO: choose a number of layers; play around with this!
    initial_angles=[0.1, 0.2],
)  # TODO: Input a list of initial guesses for the gamme_i and beta_i (all as one list). To start off, guess randomly; you can see how different initial guesses behave.
MaxCut_qaoa.train()  # runs optimization loop

# %% Finally, we can sample the resulting state using the quamtum computer (if you kept the sampler as the quantum computer above).
samples = MaxCut_qaoa.sample(sampler=sampler, shots=20_000)
print(samples)

# Find the most probable outcome
most_probable = max(samples, key=lambda y: samples[y])

# Find the cost of the most probable outcome
most_probable_cost = MaxCut_instance.quality(most_probable)

print("Cost of most probable coutcome: ", most_probable_cost)
print("Most probable outcome :", most_probable)

# %% Task: Interpret the output you get. How did the algorithm assign rooms to the students? Does it match the optimal result we found in lecture?

# We can also calculate the cost of different outputs and compare them with the optimal cost, which is calculated by classical brute force.

print(
    "Optimal cost: ", MaxCut_instance.lower_bound
)  # Classically obtain the best possible cost by brute force

# Calculate the cost function of all found solutions
samples_cost = {sample: MaxCut_instance.quality(sample) for sample in samples}

# Find the sample with the best quality
best_sample = min(samples_cost, key=lambda y: samples_cost[y])

# Find the best quality
best_quality = samples_cost[best_sample]

print("Best sample found by QAOA: ", best_sample)
print("Best cost found by QAOA: ", best_quality)

# %% Using some built-in MaxCut functionality
# The IQM QAOA package has a lot of functionality that automates creating and solving MaxCut problems. It can generate random instances of MaxCut using maxcut_generator, solve them classically, and solve them with QAOA for comparison. Below is a code snippet for this.

# Task: Finish the code snippet. Play around with it!

problem_size = 14  # Number of nodes (students) in the graph. Some of the later code will be slow if this is above 30 or so.

# The next line returns a MaxCut problem which can be used just like our previous ConstrainedQuadraticInstance
random_MaxCut = next(maxcut_generator(n=problem_size, n_instances=1))

# Draw the graph
nx.draw(random_MaxCut.qubo_graph, with_labels=True)

# Classically obtain the best possible cost by brute force
print("Optimal cost: ", random_MaxCut.lower_bound)

# %% TODO: Adapt the earlier code to run QAOA on the randomly generated graph above. How well did QAOA do?
nx.draw(MaxCut_instance.qubo_graph, with_labels=True)
print("Optimal cost: ", MaxCut_instance.lower_bound)


# %% Homework: Grover's algorithm
# Define the oracle
# This oracle tags the state |2> by changing its phase by pi.
def oracle(qv, phase=np.pi):
    tag_state({qv: 2}, phase=phase)


# Define the QuantumFloat representing the search space
n = 3
qf = QuantumFloat(n)

# Execute Grover's algorithm
grovers_alg(qf, oracle, exact=True, winner_state_amount=1)

# Retrieve the measurements
simulator_res = qf.get_measurement()
print("Simulator result: ", simulator_res)

meas_res = qf.get_measurement(backend=quantum_computer)
print("Quantum Computer result: ", meas_res)

# %%
# Copyright 2025 IQM Quantum Computers (Stefan Seegerer)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
