import numpy as np
import multiprocessing
import time

class Landscape:
    def __init__(self, N, K):
        self.N = N
        self.K = K
        self.influence_matrix = self.generate_influence_matrix()
        self.random_values = self.generate_random_values()
        self.fitness_landscape()


    def generate_influence_matrix(self):
        influence_matrix = np.eye(self.N, dtype=int)
        for row in range(self.N):
            off_diagonal_indices = np.delete(np.arange(self.N), row)
            chosen_indices = np.random.choice(off_diagonal_indices, self.K, replace=False)
            influence_matrix[row, chosen_indices] = 1
        return influence_matrix


    def generate_random_values(self):
        num_values = 2 ** (self.K + 1)
        # Create a 2D array (matrix) with 2^(K+1) rows and N columns
        return np.random.uniform(0, 1, (num_values,self.N))
        
    def generate_fitness(self, state, influence_matrix):
        state_array = np.array(state)
        fitness_values = np.zeros(self.N)

        for i in range(self.N):
            influenced_indices = np.nonzero(influence_matrix[i])[0]
            k_index = state_array[influenced_indices].dot(1 << np.arange(influenced_indices.size)[::-1])
            fitness_values[i] = self.random_values[k_index, i]
    
        return np.mean(fitness_values)
    
    def calculate_all_fitnesses(self):
        # Generate all possible states
        all_states = [np.array(list(map(int, bin(i)[2:].zfill(self.N)))) for i in range(2**self.N)]

        # Calculate fitness for each state
        all_fitnesses = [self.generate_fitness(state, self.influence_matrix) for state in all_states]
        all_fitnesses = np.array(all_fitnesses)
        return all_fitnesses
    
    def one_bit_neighbors(self, integer_position):
        bitmasks = 1 << np.arange(self.N)
        neighbors = integer_position ^ bitmasks
        return neighbors
    
    def fitness_landscape(self):
        self.performance = self.calculate_all_fitnesses()
        local_peak = np.empty(2**self.N, dtype=bool)
        all_neighbors = [self.one_bit_neighbors(pos) for pos in range(2**self.N)]
        
        for tmp_pos in range(2**self.N-1):
            tmp_neighbors = all_neighbors[tmp_pos]
            neighbors_performance = [self.performance[n] for n in tmp_neighbors]
            max_neighbor = max(neighbors_performance)
    
            local_peak[tmp_pos] = self.performance[tmp_pos] >= max_neighbor

    
        self.local_peak = local_peak
        local_peak_series = self.performance[self.local_peak]
        self.global_peak = max(self.performance)
        self.num_local_peaks = len(local_peak_series)
        self.local_peak_performance = np.mean(local_peak_series)
        
        
#####################################

def simulate_landscape(params):
    N, K = params
    landscape = Landscape(N, K)
    return landscape.num_local_peaks, landscape.global_peak, landscape.local_peak_performance

def run_landscapes_parallel(T, N, K):
    pool = multiprocessing.Pool(processes=9)
    params = [(N, K) for _ in range(T)]

    results = pool.map(simulate_landscape, params)
    pool.close()
    pool.join()


    # Unpacking results and calculating averages
    total_num_local_peaks, total_global_peak, total_local_peak_performance = 0, 0, 0
    for num_local_peaks, global_peak, local_peak_performance in results:
        total_num_local_peaks += num_local_peaks
        total_global_peak += global_peak
        total_local_peak_performance += local_peak_performance

    average_num_local_peaks = total_num_local_peaks / T
    average_global_peak = total_global_peak / T
    average_local_peak_performance = total_local_peak_performance / T

    return average_num_local_peaks, average_global_peak, average_local_peak_performance

if __name__ == "__main__":
    T = 1000  # Test with just 1 iteration
    N = 12
    K = 11
    
    start_time = time.time()

    # Run the parallel processing function
    average_num_local_peaks, average_global_peak, average_local_peak_performance = run_landscapes_parallel(T, N, K)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Parallel processing took {duration} seconds.")

    print("Average Number of Local Peaks:", average_num_local_peaks)
    print("Average Global Peak:", average_global_peak)
    print("Average Local Peak Performance:", average_local_peak_performance)