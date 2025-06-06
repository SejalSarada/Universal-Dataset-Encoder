# -*- coding: utf-8 -*-
"""Single-state prep.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RRW7hsnUaSNiKK0_kpyuYigVHyW7Sg5P
"""

!pip install torch
!pip install pennylane

"""Importing all libraries"""

import pennylane as qml
import numpy as np
import torch
from torch.autograd import Variable
import math
import matplotlib.pyplot as plt
np.random.seed(42)

import torchvision
from torchvision import datasets, transforms

"""Importing required dataset to be encoded ; here MNIST is being used"""

# Load required dataset ; here MNIST dataset is being used
mnist = datasets.MNIST(root='./data', train=True, download=True)

# Get single image
image, _ = mnist[0]

# Convert image to numpy array and flatten
image_array = np.array(image).flatten()

# Create padded tensor
state = torch.zeros(1024, dtype=torch.float32)
state[:784] = torch.from_numpy(image_array)

states = torch.tensor(state, requires_grad=False)
states = states / torch.sqrt(torch.sum(states**2))

"""Defining number of layers to be used -- CHANGE IF NEEDED
Calculating ancilla qubits
"""

numOfStates = 1
ancilla = numOfStates - len(states[0]) + 2

# number of qubits in the circuit
nr_qubits = int(np.log2(len(states))) + ancilla
# number of layers in the circuit
nr_layers = 12

# # randomly initialize parameters from a normal distribution
params = np.random.normal(0, np.pi, (nr_qubits, nr_layers, 2))
params = Variable(torch.tensor(params), requires_grad=True)

"""Next 2 blocks of code: preparing the circuit"""

# a layer of the circuit ansatz
def layer(params, j):
    for i in range(nr_qubits):
        qml.RY(params[i, j, 0], wires=i)

    for i in range(nr_qubits):
      if(i!=nr_qubits-1):
        qml.CRX(params[i, j, 1], wires=[i, i + 1])
      else:
        qml.CRX(params[i, j, 1], wires=[i, 0])

# ---- CHANGE IF NUMBER OF QUBITS, ANCILLA, STATES CHANGES --- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
dev = qml.device("default.qubit", wires=nr_qubits)

@qml.qnode(dev, interface="torch")
def circuit(params):

    qml.Barrier(wires=range(nr_qubits))

    for i in range(nr_qubits):
        qml.Hadamard(wires=i)

    # repeatedly apply each layer in the circuit
    for j in range(nr_layers):
        layer(params, j)

    for i in range(nr_qubits):
        qml.Hadamard(wires=i)

    return qml.probs(wires=range(nr_qubits))

"""To get fidelity values for plots"""

def fid_val(params):

  circuit_output = circuit(params)**(0.5)
  # print(circuit_output)
  target_state = states
  # print(target_state)
  target_state = target_state.type(circuit_output.dtype)

  # Calculate a and b
  # a = torch.sqrt(torch.abs(circuit_output[0])**2 + torch.abs(circuit_output[1])**2 + torch.abs(circuit_output[2])**2 + torch.abs(circuit_output[3])**2)

  # Calculate |ψ'⟩ and |E⟩
  # psi_dash = torch.tensor([circuit_output[0]/a, circuit_output[1]/a, circuit_output[2]/a, circuit_output[3]/a])

  # Calculate innerproduct fidelity
  fidelity = torch.abs(torch.dot(circuit_output.conj(), target_state))**2

  return (fidelity.detach().numpy())

"""fidelity cost calculation for non-ancilla (non-commented) and ancilla(commented) circuits"""

def fidelity_cost(params):
  cost=0

  circuit_output = circuit(params)**(0.5)
  # print(circuit_output)
  target_state = states
  # print(target_state)
  target_state = target_state.type(circuit_output.dtype)

  # Calculate a and b
  # a = torch.sqrt(torch.abs(circuit_output[0])**2 + torch.abs(circuit_output[1])**2 + torch.abs(circuit_output[2])**2 + torch.abs(circuit_output[3])**2)

  # Calculate |ψ'⟩ and |E⟩
  # psi_dash = torch.tensor([circuit_output[0]/a, circuit_output[1]/a, circuit_output[2]/a, circuit_output[3]/a])

  # Calculate innerproduct fidelity
  fidelity = torch.abs(torch.dot(circuit_output.conj(), target_state))**2

  # Convert fidelity to cost (1 - fidelity)
  # cost = 0.1*(1 - (torch.abs(a))**2) + 0.9*(1 - (fidelity))
  # state_cost = 1 - ((torch.abs(a))**2)*fidelity
  cost = 1 - fidelity

  return cost

"""Calculating mse cost"""

# def mse_cost(params):
#   cost=0

#   circuit_output = circuit(params)**(0.5)
#   target_state = states
#   target_state = target_state.type(circuit_output.dtype)

#   # Calculate a and b
#   # a = torch.sqrt(torch.abs(circuit_output[0])**2 + torch.abs(circuit_output[1])**2 + torch.abs(circuit_output[2])**2 + torch.abs(circuit_output[3])**2)

#   # Calculate |ψ'⟩ and |E⟩
#   # psi_dash = torch.tensor([circuit_output[0]/a, circuit_output[1]/a, circuit_output[2]/a, circuit_output[3]/a])

#   mse_cost = (torch.sum((circuit_output - target_state)**2)) / numOfStates

#   cost = mse_cost

#   return cost

"""calculating l1 cost"""

# def l1_cost(params):
#   cost=0

#   circuit_output = circuit(params)**(0.5)
#   target_state = states
#   target_state = target_state.type(circuit_output.dtype)

#   # Calculate a and b
#   # a = torch.sqrt(torch.abs(circuit_output[0])**2 + torch.abs(circuit_output[1])**2 + torch.abs(circuit_output[2])**2 + torch.abs(circuit_output[3])**2)

#   # Calculate |ψ'⟩ and |E⟩
#   # psi_dash = torch.tensor([circuit_output[0]/a, circuit_output[1]/a, circuit_output[2]/a, circuit_output[3]/a])

#   l1_cost = (torch.sum(torch.abs(circuit_output - target_state))) / numOfStates

#   cost = l1_cost

#   return cost

"""Running the model for the suitable cost ; here Fidelity cost is being used"""

loss_values = []
iteration_values = []
fidelity_values = []

# set up the optimizer - RPROP OR ADAMW
opt = torch.optim.Rprop([params])

# number of steps in the optimization routine
steps = 500

# the final stage of optimization isn't always the best, so we keep track of
# the best parameters along the way
best_cost = fidelity_cost(params)
best_params = np.zeros((nr_qubits, nr_layers, 2))
loss_values.append(best_cost.detach().numpy())
fidelity_values.append(1 - (best_cost.detach().numpy()))
iteration_values.append(0)

print("Cost after 0 steps is {:.4f}".format(fidelity_cost(params)))

# optimization begins
for n in range(steps):
    opt.zero_grad()
    loss = fidelity_cost(params)
    loss.backward()
    opt.step()

    loss_values.append(loss.item())  # Get the scalar value of the loss as a Python number
    fidelity_values.append(1 - (loss.item()))
    iteration_values.append(n + 1)

    # keeps track of best parameters
    if loss < best_cost:
        best_cost = loss
        best_params = params

    # Keep track of progress every 10 steps
    if n % 10 == 9 or n == steps - 1:
        print("Cost after {} steps is {:.4f}".format(n + 1, loss))

plt.plot(iteration_values, fidelity_values)
plt.xlabel("Iteration")
plt.ylabel("Fidelity")
plt.title("Fidelity vs. Iteration")
plt.show()

"""To get the states produced if Fidelity cost is used (Also CHANGE IF ANCILLA qubits are used)"""

circuit_output = circuit(best_params)**(0.5)
target_state = states
target_state = target_state.type(circuit_output.dtype)
print(circuit_output)
  # Calculate a and b
# a = torch.sqrt(torch.abs(circuit_output[0])**2 + torch.abs(circuit_output[1])**2 + torch.abs(circuit_output[2])**2 + torch.abs(circuit_output[3])**2)

  # Calculate |ψ'⟩ and |E⟩
# psi_dash = torch.tensor([circuit_output[0]/a, circuit_output[1]/a, circuit_output[2]/a, circuit_output[3]/a])
# print(psi_dash)
print(target_state)
  # Calculate innerproduct fidelity
print()
fidelity = torch.abs(torch.dot(circuit_output.conj(), target_state))**2
print(fidelity)

  # Convert fidelity to cost (1 - fidelity)
# cost = 0.1*(1 - (torch.abs(a))**2) + 0.9*(1 - (fidelity))
cost = 1 - fidelity
print(cost)

drawer = qml.draw(circuit)
print(drawer(best_params))

