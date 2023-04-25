# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/feature_space_plotting.ipynb.

# %% auto 0
__all__ = ['plot_dataset_embedding']

# %% ../nbs/feature_space_plotting.ipynb 5
import numpy as np
from fastai.vision.all import *
import matplotlib.pyplot as plt

# %% ../nbs/feature_space_plotting.ipynb 6
def plot_dataset_embedding(dataset: Datasets, feature_extractor, num_samples_per_class=300, normalize_features=False, *args, **kwargs):
    COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    feature_extractor.eval()

    with torch.no_grad():
        for c, ss in dataset.by_target.items():
            color = COLORS[dataset.vocab.o2i[c] % len(COLORS)]
            samples = ss.random_sub_dsets(num_samples_per_class).load()[0]
            embeddings = feature_extractor(samples)
            if normalize_features:
                embeddings = torch.nn.functional.normalize(embeddings, dim=1)

            _plot_cluster(embeddings.cpu().numpy(), color, label=c, *args, **kwargs)

    plt.legend()

def _plot_cluster(points: ndarray, color, *args, **kwargs):
    assert points.ndim == 2 and points.shape[1] == 2
    plt.scatter(*points.transpose(), color=color, *args, **kwargs)
