import time
import json
import hashlib
import tracemalloc
import random
import string

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def generate_random_transaction():
    return {
        "sender": "".join(random.choices(string.ascii_uppercase, k=5)),
        "receiver": "".join(random.choices(string.ascii_uppercase, k=5)),
        "amount": round(random.uniform(1, 1000), 2),
    }


def generate_classical_hash(data: str):
    return hashlib.sha256(data.encode()).hexdigest()


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


def benchmark_multiple_blocks(method_name, hash_function, transaction_list):
    print(f"\n Starting: {method_name} for {len(transaction_list)} blocks...")
    tracemalloc.start()
    total_time = 0
    block_hashes = []

    for transaction in transaction_list:
        transaction_str = json.dumps(transaction, sort_keys=True)

        start_time = time.perf_counter()
        block_hash = hash_function(transaction_str)
        end_time = time.perf_counter()

        block_hashes.append(block_hash)
        total_time += end_time - start_time

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "method": method_name,
        "total_time_sec": round(total_time, 4),
        "avg_time_sec": round(total_time / len(transaction_list), 6),
        "memory_peak_kb": round(peak / 1024, 2),
        "sample_blocks": block_hashes[:5],
    }


def qrng(bit_count=128):
    qc = QuantumCircuit(bit_count, bit_count)
    qc.h(range(bit_count))
    qc.measure(range(bit_count), range(bit_count))

    simulator = AerSimulator()
    job = simulator.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()
    bitstring = list(counts.keys())[0]

    return bitstring


def gen_qrng():
    bit = qrng()
    doi = hashlib.sha256(bit.encode()).hexdigest()[:10]
    return doi


if __name__ == "__main__":
    print(f"Generated DOI: {gen_qrng()}")

# if __name__ == "__main__":
    # transaction_list = [generate_random_transaction() for _ in range(100)]

    # classical_results = benchmark_multiple_blocks(
    #     "Classical Hashing", generate_classical_hash, transaction_list
    # )
    # quantum_results = benchmark_multiple_blocks(
    #     "Quantum Hashing", lambda _: generate_quantum_hash(), transaction_list
    # )

    # print(f"\n=== Benchmark Results ===")
    # print(json.dumps([classical_results, quantum_results], indent=4))