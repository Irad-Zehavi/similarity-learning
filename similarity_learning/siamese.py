# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/siamese.ipynb.

# %% auto 0
__all__ = ['normalized_squared_euclidean_distance', 'ContrastiveLoss', 'DistanceSiamese']

# %% ../nbs/siamese.ipynb 4
from torch import nn
from torch.nn.functional import normalize

from fastai.vision.all import *


def normalized_squared_euclidean_distance(x1, x2):
    r"""
    Squared Euclidean distance over normalized vectors:
    $$\left\| \frac{x_1}{\|x_1\|}-\frac{x_2}{\|x_2\|} \right\|^2 $$
    """
    assert x1.dim() <= 2
    assert x2.dim() <= 2
    x1 = normalize(x1, dim=-1)
    x2 = normalize(x2, dim=-1)
    return (x1 - x2).pow(2).sum(dim=-1)


class ContrastiveLoss(BaseLoss):
    @delegates(nn.HingeEmbeddingLoss)
    def __init__(self, **kwargs):
        super().__init__(loss_cls=nn.HingeEmbeddingLoss, **kwargs)

    def __call__(self, input, target):
        return super().__call__(input, 2*target-1)  # hinge_embedding_loss expects targets to be 1 or -1


# @dataclass
class DistanceSiamese(Module):
    """Outputs the distance between two inputs in feature space"""
    def __init__(self, 
                 backbone: Module,  # embeds inputs in a feature space
                 distance_metric = normalized_squared_euclidean_distance):
        self.backbone = backbone
        self.distance_metric = distance_metric

    def forward(self, x):
        f1, f2 = L(x).map(self.backbone).map(nn.Flatten())
        return self.distance_metric(f1, f2)


# %% ../nbs/siamese.ipynb 5
from matplotlib.ticker import PercentFormatter
from tqdm.autonotebook import tqdm
import numpy as np

@patch
def plot_distance_histogram(self: DistanceSiamese, pairs_dl: TfmdDL, label='Distance'):
    """Plots a histogram of intra-class and inter-class distances"""
    self.eval().to(pairs_dl.device)
    
    with torch.no_grad():
        processed_batches = [(self(x), y) for x, y in tqdm(pairs_dl, desc='Computing distances')]
        distances, targets = [torch.cat(o).cpu().numpy() for o in zip(*processed_batches)]

    _hist(distances[targets==1], 'Intra-Class')
    _hist(distances[targets==0], 'Inter-Class')
    
    plt.legend()
    plt.xlabel(label)

def _hist(distances, label=None):
    weights = np.ones_like(distances) / len(distances)  # normalization for percentage ticks
    plt.hist(distances, label=label, alpha=.5, edgecolor='black', lw=1, weights=weights)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
