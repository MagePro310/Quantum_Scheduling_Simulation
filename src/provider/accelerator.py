"""Wrapper for IBMs backend simulator."""
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit

from src.common.ibmq_backend import IBMQBackend
from src.tools import optimize_circuit_online


class Accelerator:
    """Wraper for a single backend simulator."""

    def __init__(
        self, backend: IBMQBackend, shot_time: int = 1, reconfiguration_time: int = 0
    ) -> None:
        self.simulator = AerSimulator.from_backend(backend.value())
        self._backend = backend
        self._qubits = len(self.simulator.properties().qubits)
        self._shot_time = shot_time
        self._reconfiguration_time = reconfiguration_time
        
    @property
    def shot_time(self) -> int:
        """Time factor for each shot.

        Returns:
            int: The time one shot takes.
        """
        return self._shot_time
    
    @property
    def reconfiguration_time(self) -> int:
        """Additional time penalty for reconfiguration.

        Returns:
            int: The recongiguration time.
        """
        return self._reconfiguration_time  
    
    @property
    def qubits(self) -> int:
        """Number of qubits.

        Returns:
            int: The number of qubits.
        """
        return self._qubits

    @property
    def backend(self) -> IBMQBackend:
        """The backend, which is simulated.

        Returns:
            IBMQBackend: The backend.
        """
        return self._backend
    
    
    def run_and_get_counts(
        self, circuit: QuantumCircuit, n_shots: int = 2**10
        ) -> dict[str, int]:
        """Run a circuit and get the measurment counts.

        The circuit is optimized before running, using the now available backend information.
        Args:
            circuit (QuantumCircuit): The circuit to run.
            n_shots (int, optional): Number of shots. Defaults to 2**10.

        Returns:
            dict[str, int]: Measurment counts.
        """
        
        # TODO check qubit size
        #opt_circuit = optimize_circuit_online(circuit, self._backend) # Have some problems with blocking here
        #result = self.simulator.run(opt_circuit).result()
            
        #circuit = optimize_circuit_online(circuit, self._backend)      
        result = self.simulator.run(circuit, shots=n_shots).result()
        
        return result.get_counts(0)