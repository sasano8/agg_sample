from transformers import PyTorchBenchmark, PyTorchBenchmarkArguments

# pytorch
args = PyTorchBenchmarkArguments(models=["bert-base-uncased"], batch_sizes=[8], sequence_lengths=[8, 32, 128, 512])
benchmark = PyTorchBenchmark(args)



if __name__ == "__main__":
    # python examples/pytorch/benchmarking/run_benchmark.py --help
    results = benchmark.run()
    # デフォルトでは、推論に必要な時間とメモリがベンチマークされます。


py3nvml