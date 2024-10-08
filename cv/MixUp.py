import numpy as np
from numba import njit


@njit
def sample_beta_distribution(
    size: int, concentration_0: float = 0.2, concentration_1: float = 0.2
) -> np.ndarray:
    """
    Samples from a beta distribution.

    Args:
        size (int): Size of the sample.
        concentration_0 (float): Concentration parameter of the first gamma distribution.
        concentration_1 (float): Concentration parameter of the second gamma distribution.

    Returns:
        numpy.ndarray: Sample from the beta distribution.
    """

    gamma_1_sample = np.array([np.random.gamma(concentration_1) for _ in range(size)])
    gamma_2_sample = np.array([np.random.gamma(concentration_0) for _ in range(size)])

    return gamma_1_sample / (gamma_1_sample + gamma_2_sample)


@njit
def mix_up(ds_one: tuple, ds_two: tuple, alpha: float = 0.2) -> tuple:
    """
    Performs mixup augmentation on a pair of datasets.

    Args:
        ds_one (tuple): Tuple containing images and labels from the first dataset.
        ds_two (tuple): Tuple containing images and labels from the second dataset.
        alpha (float): Hyperparameter controlling the mixup ratio.

    Returns:
        tuple: Augmented images and corresponding labels.
    """

    # Unpack two datasets
    images_one, labels_one = ds_one
    images_two, labels_two = ds_two
    batch_size = images_one.shape[0]

    # Sample lambda and reshape it to do the mixup
    l = sample_beta_distribution(batch_size, alpha, alpha)
    x_l = l.reshape((batch_size, 1, 1, 1))
    y_l = l.reshape((batch_size, 1))

    # Perform mixup on both images and labels by combining a pair of images/labels
    # (one from each dataset) into one image/label
    images = images_one * x_l + images_two * (1 - x_l)
    labels = labels_one * y_l + labels_two * (1 - y_l)

    return images, labels
