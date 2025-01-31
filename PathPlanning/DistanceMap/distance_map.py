"""
Distance Map

author: Wang Zheng (@Aglargil)

Ref:

- [Distance Map]
(https://cs.brown.edu/people/pfelzens/papers/dt-final.pdf)
"""

import numpy as np
import matplotlib.pyplot as plt

INF = 1e20


def compute_sdf(bool_field):
    """
    Compute the signed distance field (SDF) from a boolean field.

    Parameters
    ----------
    bool_field : array_like
        A 2D boolean array where '1' represents obstacles and '0' represents free space.

    Returns
    -------
    array_like
        A 2D array representing the signed distance field, where positive values indicate distance
        to the nearest obstacle, and negative values indicate distance to the nearest free space.
    """
    a = compute_udf(bool_field)
    b = compute_udf(bool_field == 0)
    return a - b


def compute_udf(bool_field):
    """
    Compute the unsigned distance field (UDF) from a boolean field.

    Parameters
    ----------
    bool_field : array_like
        A 2D boolean array where '1' represents obstacles and '0' represents free space.

    Returns
    -------
    array_like
        A 2D array of distances from the nearest obstacle, with the same dimensions as `bool_field`.
    """
    edt = bool_field.copy()
    edt = np.where(edt == 0, INF, edt)
    edt = np.where(edt == 1, 0, edt)
    for row in range(len(edt)):
        dt(edt[row])
    edt = edt.T
    for row in range(len(edt)):
        dt(edt[row])
    edt = edt.T
    return np.sqrt(edt)


def dt(d):
    """
    Compute 1D distance transform under the squared Euclidean distance

    Parameters
    ----------
    d : array_like
        Input array containing the distances.

    Returns:
    --------
    d : array_like
        The transformed array with computed distances.
    """
    v = np.zeros(len(d) + 1)
    z = np.zeros(len(d) + 1)
    k = 0
    v[0] = 0
    z[0] = -INF
    z[1] = INF
    for q in range(1, len(d)):
        s = ((d[q] + q * q) - (d[int(v[k])] + v[k] * v[k])) / (2 * q - 2 * v[k])
        while s <= z[k]:
            k = k - 1
            s = ((d[q] + q * q) - (d[int(v[k])] + v[k] * v[k])) / (2 * q - 2 * v[k])
        k = k + 1
        v[k] = q
        z[k] = s
        z[k + 1] = INF
    k = 0
    for q in range(len(d)):
        while z[k + 1] < q:
            k = k + 1
        dx = q - v[k]
        d[q] = dx * dx + d[int(v[k])]


def main():
    bool_field = np.array(
        [
            [1, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )

    # Compute the signed distance field
    sdf = compute_sdf(bool_field)
    udf = compute_udf(bool_field)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    ax1.imshow(bool_field, cmap="binary")
    ax1.set_title("Boolean Field")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")

    udf_plot = ax2.imshow(udf, cmap="viridis")
    ax2.set_title("Unsigned Distance Field")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    plt.colorbar(udf_plot, ax=ax2)

    sdf_plot = ax3.imshow(sdf, cmap="RdBu")
    ax3.set_title("Signed Distance Field")
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    plt.colorbar(sdf_plot, ax=ax3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
