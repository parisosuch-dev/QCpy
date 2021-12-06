"""
QuantumCircuit.py

Sources:
https://en.wikipedia.org/wiki/Quantum_logic_gate
"""
from .Qubit import Qubit
from .Graph import *
import numpy as np
from math import sqrt

class QuantumCircuit:
    def __init__(self, bit_str: str):
        self._bit_str = bit_str # string of qubits bits in system
        self._qubit_array = [] # array holding qubits
        # using bit_str, generate qubits and add to array
        bits = [char for char in bit_str]
        for bit in bits:
            qb = Qubit(int(bit))
            self._qubit_array.append(qb)
    def identity(self, bit: int):
        """
        Identity-Gate Operation on specified qubit.
        Params:
            bit (int): the nth-bit position on circuit.
        Returns:
            None
        """
        # pull out qubit at bit position in self._qubit_array[bit]
        temp_arr = self._qubit_array[bit].state
        # multiply the NOT gate against the qubit.state array
        identity_gate = [[1+0j, 0+0j], [0+0j, 1+0j]]
        temp_arr = np.dot(identity_gate, temp_arr)
        # put result of that product back in to the self._qubit_array[bit]
        self._qubit_array[bit].state = temp_arr
    def x(self, bit: int):
        """
        Pauli-X-Gate Operation on specified qubit.
        Params:
            bit (int): the nth-bit position on circuit.
        Returns:
            None
        """
        # pull out qubit at bit position in self._qubit_array[bit]
        temp_arr = self._qubit_array[bit].state
        # multiply the NOT gate against the qubit.state array
        x_gate = [[0+0j, 1+0j], [1+0j, 0+0j]]
        temp_arr = np.dot(x_gate, temp_arr)
        # put result of that product back in to the self._qubit_array[bit]
        self._qubit_array[bit].state = temp_arr
    def y(self, bit: int):
        """
        Pauli-Y-Gate Operatrion on specified qubit.
        Params:
            bit (int): the nth-bit position on circuit.
        Returns:
            None
        """
        # pull out qubit at bit position in self._qubit_array[bit]
        temp_arr = self._qubit_array[bit].state
        # multiply the Y gate against the qubit.state array
        y_gate = [[0+0j, 0-1j], [0+1j, 0+0j]]
        temp_arr = np.dot(y_gate, temp_arr)
        # put result of that product back in to the self._qubit_array[bit]
        self._qubit_array[bit].state = temp_arr
    def z(self, bit: int):
        """
        Pauli-Z-Gate Operation on specifid qubit.
        Params:
            bit (int): the nth-bit position on circuit.
        Returns:
            None
        """
        # pull out qubit at bit position in self._qubit_array[bit]
        temp_arr = self._qubit_array[bit].state
        # multiply the Z gate against the qubit.state array
        z_gate = [[1+0j, 0+0j], [0+0j, -1+0j]]
        temp_arr = np.dot(z_gate, temp_arr)
        # put result of that product back in to the self._qubit_array[bit]
        self._qubit_array[bit].state = temp_arr
    def hadamard(self, bit: int):
        """
        Hadamard-Gate Operation on specifid qubit.
        Params:
            bit (int): the nth-bit position on circuit.
        Returns:
            None
        """
        # pull out qubit at bit position in self._qubit_array[bit]
        temp_arr = self._qubit_array[bit].state
        # multiply the Hadamard gate against the qubit.state array
        hadamard_gate = np.array([[1+0j, 1+0j], [1+0J, -1+0j]]) * 1/sqrt(2)
        temp_arr = np.dot(hadamard_gate, temp_arr)
        # put result of that product back in to the self._qubit_array[bit]
        self._qubit_array[bit].state = temp_arr
    def measure(self):
        """
        Collapses quantum circuit into classical bits.
        Params:
            None
        Returns:
            final_state (str): classical bits
        """
        # get probabilities matrix from self.probabilities()
        probability_matrix = self.probabilities()
        # create a 1D array of the states, 2 ** n(qubits)
        num_bits = len(self._qubit_array)# number of bits
        state_list = [format(i, 'b').zfill(num_bits) for i in range(2**num_bits)] # creates a list of bits in strings
        state_list = list(map(int, state_list)) # turns state_list from list of strings to list of ints
        # create a temporary np.array to flatten the 2D probability_matrix into a 1D array which can
        # hold all the probabilities as weights
        weight_list = probability_matrix.flatten()
        # numpy.random.choice takes in the list we will select from, size of the returning list,
        # and p = weights of each element 
        final_state = np.random.choice(state_list, 1, p = weight_list)
        final_state = str(final_state[0]) # take out the bits from the returned list and convert to a string
        final_state = final_state.zfill(num_bits) # pad with zeroes if needed
        return(final_state) # return the final state
    def probabilities(self):
        """
        Returns matrix with all probabilities for each state.
        Params:
            None
        Returns:
            probability_matrix (list): matrix with all weighted probabilities.
        """
        # make a copy of self._qubit_array states which will be used as a queue
        q = []
        for i in range(len(self._qubit_array)):
            q.append(self._qubit_array[i].state)
        temp_arr = np.array(q[0])
        if len(q) > 1: # tensor only if the length of self._qubit_array is greater than 1
            # use numpy's Kronecker product on the first 2 qubit states and then delete them from the queue
            temp_arr = np.kron(q[0], q[1])
            del q[0]
            del q[0]
            while q: # go through the rest of the queue
                temp_arr = np.kron(temp_arr, q[0])
                del q[0]
        # square all of the values to get probabilties of each qubit state
        temp_arr = np.square(temp_arr)
        # turn all the complex numbers into real numbers
        probability_matrix = np.abs(temp_arr.real)
        return(probability_matrix)
    def graph(self):
        """
        Generate a graph using probabilities().
        Params:
            None
        Returns:
            png file.
        """
        qubits_graph = Graph(self.probabilities())
        return qubits_graph.makeGraph()