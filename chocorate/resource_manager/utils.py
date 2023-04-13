import py3nvml

# gpuをコントロールする場合に使用する
py3nvml.grab_gpus(3)
py3nvml.grab_gpus(num_gpus - 2, gpu_select=[0, 1, 2, 3])


free_gpus = py3nvml.get_free_gpus()

# 1はrunning
num_procs = py3nvml.get_num_procs()
# [0, 0, 0, 0, 1, 0]
