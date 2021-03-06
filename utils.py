import torch
import numpy as np
import pandas as pd
import random

# equalize the number of samples in each set to be the sum of the size of the two sets
def equalize_union(a, b):
    c = range(len(a) + len(b))
    a, _ = equalize(a, c)
    _, b = equalize(c, b)
    return a, b

# equalize the number of samples in each set by taking random permutations of the data
def equalize(a, b):
    diff = abs(len(a) - len(b))
    if diff != 0:
        to_equalize = a if len(a) < len(b) else b
        whole_perm = []

        num_perm = int(diff / len(to_equalize))
        if num_perm:
            whole_perm = np.concatenate([np.random.permutation(to_equalize) for _ in range(num_perm)])

        remain_choice = np.random.choice(to_equalize, size=diff - len(whole_perm), replace=False)
        to_equalize = np.concatenate([to_equalize, whole_perm, remain_choice]).astype(int)

        if len(a) < len(b):
            a = to_equalize
        else: 
            b = to_equalize

    return a, b

def to_onehot(indices, num_classes):
    """Convert a tensor of indices to a tensor of one-hot indicators."""
    onehot = torch.zeros(indices.shape[0], num_classes, device=indices.device)
    return onehot.scatter_(1, indices.unsqueeze(1), 1)

def set_seed(n, use_cuda=False):
    np.random.seed(n)
    pd.np.random.seed(n)
    torch.manual_seed(n)
    random.seed(n)
    if use_cuda:
        torch.cuda.manual_seed_all(n)
