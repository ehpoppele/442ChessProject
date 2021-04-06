#include "search.h"
#include "thread.h"


__global__ void cuda_search(Thread thread) {
  return;
}

void search_on_gpu(Thread thread){
    cuda_search<<<1, 1>>>(thread);
    cudaDeviceSynchronize();
}
