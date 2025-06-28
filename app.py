from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import hashlib
import json
import time


def generate_quantum_hash(num_qubits=4):
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    qc.measure(range(num_qubits), range(num_qubits))

    simulator = AerSimulator()
    job = simulator.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()
    bitstring = list(counts.keys())[0]

    return hashlib.sha256(bitstring.encode()).hexdigest()


def create_block(previous_hash, transaction_data):
    timestamp = time.time()
    quantum_hash = generate_quantum_hash()
    block = {
        "previous_hash": previous_hash,
        "transaction_data": transaction_data,
        "timestamp": timestamp,
        "quantum_hash": quantum_hash,
    }

    block_hash = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
    return {"block": block, "block_hash": block_hash}


if __name__ == "__main__":
    transaction = {"sender": "Alice", "receiver": "Bob", "amount": 10}
    genesis_hash = "0" * 64
    block = create_block(genesis_hash, transaction)

    print("Block created:")
    print(json.dumps(block, indent=4))
