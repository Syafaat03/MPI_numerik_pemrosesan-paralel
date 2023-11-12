from mpi4py import MPI
import numpy as np
import time

def matrix_multiply(A, B):
    return np.dot(A, B)

def scatter_data(comm, data):
    size = comm.Get_size()
    rank = comm.Get_rank()
    sendbuf = None

    if rank == 0:
        sendbuf = np.array_split(data, size)

    recvbuf = comm.scatter(sendbuf, root=0)
    return recvbuf

def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Define matrices A and B
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    B = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

    if rank == 0:
        # Scatter matrix A to all processes
        local_A = scatter_data(comm, A)
    else:
        local_A = None

    # Broadcast matrix B to all processes
    local_B = comm.bcast(B, root=0)

    # Start the timer
    start_time = time.time()

    # Scatter matrix A and perform local matrix multiplication
    local_result = scatter_data(comm, local_A)
    local_result = matrix_multiply(local_result, local_B)

    # Gather the local results to the root process
    global_result = comm.gather(local_result, root=0)

    # Stop the timer
    end_time = time.time()

    if rank == 0:
        # Concatenate the global results to get the final result
        final_result = np.concatenate(global_result)
        print("Matrix A:")
        print(A)
        print("\nMatrix B:")
        print(B)
        print("\nResult of Matrix Multiplication:")
        print(final_result)
        print("\nRuntime: {} seconds".format(end_time - start_time))

if _name_ == "_main_":
    main()
