#include "../common/common.h"
#include <cuda_runtime.h>
#include <stdio.h>
#include <math.h>

/**
 * @file threadidx.cu
 * @brief
 * 
 * This is... 
 * 
 * @author Alma Zhong <almaz@andrew.cmu.edu>
 */


//this is some constant h vector for now (3D)
#define dim 3
#define hx 1
#define hy 2
#define hz 3

/**
 * @brief checks that the CPU and GPU algorithms produce the same arrays
 * 
 * @param[in] hostRef resulting array after CPU
 * @param[in] gpuRef resulting array after GPU
 * @param[in] N length of arrays
 * 
 * 
 */
void checkResult(int *hostRef, int *gpuRef, const int N)
{
    double epsilon = 1.0E-8;
    bool match = 1;

    for (int i = 0; i < N; i++)
    {
        if (abs(hostRef[i] - gpuRef[i]) > epsilon)
        {
            match = 0;
            printf("Arrays do not match!\n");
            printf("host %5.2f gpu %5.2f at current %d\n", hostRef[i],
                   gpuRef[i], i);
            break;
        }
    }

    if (match) printf("Arrays match.\n\n");

    return;
}

/**
 * @brief computes the cross product given the ith m vector and jth position
 * 
 * @param[in] A given thread array (3*N threads)
 * @param[in] vec ith m vector
 * @param[in] axis direction, x, y, or z (0, 1, 2)
 * 
 * @return the cross product
 */
__host__ __device__ int compute(int *A, int *H, int vec, int axis){

    int hidx1 = 3 * vec + (axis + 1) % dim;
    int midx1 = 3 * vec + (axis + 2) % dim;

    int hidx2 = 3 * vec + (axis + 2) % dim;
    int midx2 = 3 * vec + (axis + 1) % dim;
    
    return H[hidx1] * A[midx1] - H[hidx2] * A[midx2];

}

/** 
 * @brief cross product GPU
 * computes the index into array B to place cross product computation
 * 
 * @param[in] A array of threads
 * @param[in] B array of cross products
 * @param[in] N length of arrays
*/
__global__ void cross_productGPU(int *A, int *B, int *H, const int N){
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    if(i < N){
        int vec = i / dim; //automatically rounds down?
        int axis = i % dim;

        int hidx1 = 3 * vec + (axis + 1) % dim; 
        int midx1 = 3 * vec + (axis + 2) % dim;

        int hidx2 = 3 * vec  + (axis + 2) % dim;
        int midx2 = 3 * vec + (axis + 1) % dim;

        int res = H[hidx1] * A[midx1] - H[hidx2] * A[midx2];
        //- (m x h)

        B[i] = -1 * res;
    }

}

/** 
 * @brief cross product CPU
 * traverses array B to place cross product computation
 * 
 * @param[in] A array of threads
 * @param[in] B array of cross products
 * @param[in] N length of arrays
*/
void cross_productCPU(int *A, int *B, int *H, const int N)
{
    for (int idx = 0; idx < N; idx++){
        int vec = idx / dim;
        int axis = idx % dim;

        B[idx] = -1 * compute(A, H, vec, axis);
    }
}


void initialData(int *arr, int size){
    // generate different seed for random number
    time_t t;
    srand((unsigned) time(&t));

    for (int i = 0; i < size; i++)
    {
        arr[i] = (int)(rand() & 0xFF) / 10.0f;
    }

    return;
}

int main(int argc, char **argv){
    
    printf("%s Starting...\n", argv[0]);

    //set up device
    int dev = 0;
    cudaDeviceProp deviceProp;
    CHECK(cudaGetDeviceProperties(&deviceProp, dev));
    printf("Using Device %d: %s\n", dev, deviceProp.name);
    CHECK(cudaSetDevice(dev));

    //how many m vectors 
    int nElem = 1000000;

    //how many threads
    int N = nElem * dim;

    printf("there are %d m vectors\n", nElem);
    printf("there are %d threads for %d dimensions\n", N, dim);

    //3N threads
    size_t bytes = N * sizeof(int); 
    //size_t bytes2 = nElem * sizeof(float); 

    //host memory
    int *h_A, *h_B, *gpuRef, *cpuRef;

    h_A = (int*)malloc(bytes); //m vector
    h_B = (int*)malloc(bytes); //h vector

    //for vectors
    //h_B = (float*)malloc(bytes2);
    gpuRef = (int*)malloc(bytes);
    cpuRef = (int*)malloc(bytes);

    initialData(h_A, N);
    initialData(h_B, N);

    memset(gpuRef, 0, bytes); //cross product
    memset(cpuRef, 0, bytes);

    double istart = seconds();
    cross_productCPU(h_A, cpuRef, h_B, N);
    double cpuTime = seconds() - istart;
    printf("CPU elapse %f sec\n", cpuTime);

    //device memory
    int *d_A, *d_B, *d_C;
    CHECK(cudaMalloc((int**)&d_A, bytes)); //m vector
    CHECK(cudaMalloc((int**)&d_B, bytes)); //cross product
    CHECK(cudaMalloc((int**)&d_C, bytes)); //h vector
    //CHECK(cudaMalloc((float**)&d_C, bytes2));

    //transfer data from host to device
    CHECK(cudaMemcpy(d_A, h_A, bytes, cudaMemcpyHostToDevice)); //m vector
    CHECK(cudaMemcpy(d_C, h_B, bytes, cudaMemcpyHostToDevice)); //h vector
    CHECK(cudaMemcpy(d_B, gpuRef, bytes, cudaMemcpyHostToDevice)); //is this right?

    //invoke kernel at host side
    int dimx = 256;
    dim3 block (dimx);
    dim3 grid ((N + block.x - 1) / block.x);

    istart = seconds();
    cross_productGPU<<<grid, block>>>(d_A, d_B, d_C, N);
    CHECK(cudaDeviceSynchronize());
    double gpuTime = seconds() - istart;
    printf("GPU <<<(%d), (%d)>>> elapse %f sec\n", grid.x, block.x, gpuTime);

    printf("speedup: %.2fx\n", cpuTime / gpuTime);

    //copy kernel result back to host side
    CHECK(cudaMemcpy(gpuRef, d_B, bytes, cudaMemcpyDeviceToHost));

    //perform on CPU
    //cross_productCPU(h_A, cpuRef, h_B, N);

    checkResult(cpuRef, gpuRef, N);

    //free memory
    CHECK(cudaFree(d_A));
    CHECK(cudaFree(d_B));

    free(h_A);
    free(gpuRef);
    free(cpuRef);

    CHECK(cudaDeviceReset());
    return 0;

}

