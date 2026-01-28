This project (May 2025 - August 2025) implements a parallel CUDA kernel intended to compute cross products for magentization vectors and magnetic field vectors in 3D space.
To develop magnetic field simulations with millions of grid point calculations, this implementation achieves over 57x speedup for vector cross products at a large scale.
Mentored under Prof. Jimmy Zhu at Carnegie Mellon University.

results for 3M threads, 1M inputs
CPU: 5.3 milliseconds
GPU: 93 microseconds

index threads using vector (/3) and axis (%3) to avoid branching
