from networkx.algorithms.core import k_core
from skimage import data
import math
import numpy as np
from PIL import Image
from sklearn.cluster import AgglomerativeClustering

img = data.coffee() # 400, 600, 3
cropped_img = np.array(img, dtype=np.float64)
h, w, channels = cropped_img.shape
original_size_bits = h * w * channels * 8

k_values = [6, 10, 14]
c_values = [20, 50, 80]


for c in c_values:
    num_blocks_h = h // c
    num_blocks_w = w // c
    N = num_blocks_h * num_blocks_w

    h = (h // c) * c
    w = (w // c) * c
    cropped_img = cropped_img[:h, :w, :]

    blocks = []
    for i in range(num_blocks_h):
        for j in range(num_blocks_w):
            block = cropped_img[i * c : (i + 1) * c, j * c : (j + 1) * c, :]
            blocks.append(block.flatten(order="F"))


    X = np.array(blocks)  # shape: (N, c * c * 3)
    print("blocks shape", X.shape)

    for k in k_values:
        print(f"Running c={c}, k={k} (N={N} windows)...")

        # build the dendrogram, and cut the tree to k clusters
        clustering = AgglomerativeClustering(n_clusters=k, linkage="single", metric="euclidean")
        labels = clustering.fit_predict(X)

        # build the sample vector for the k clusters
        codebook = np.zeros((k, c * c * channels), dtype=np.float64)
        for cluster_id in range(k):
            mask = (labels == cluster_id)
            codebook[cluster_id] = np.mean(X[mask], axis=0)

        # assigned the labels to the corresponding codebook vectors
        reconstructed_blocks = codebook[labels]

        # img rebuild
        reconstructed_img = np.zeros((h, w, channels), dtype=np.float64)
        idx = 0
        for i in range(num_blocks_h):
            for j in range(num_blocks_w):
                block = reconstructed_blocks[i*num_blocks_w+j].reshape((c, c, channels), order="F")
                reconstructed_img[i*c : (i+1)*c, j*c : (j+1)*c, : ] = block

        # (a) save img
        reconstructed_uint8 = np.clip(np.round(reconstructed_img), 0, 255).astype(np.uint8)
        Image.fromarray(reconstructed_uint8).save(f"HW2_1-1/HW2_1-1_1-coffee_c{c}_k{k}.png")

        # (b) Reconstruction Error/ SSD
        ssd_error = np.sum((cropped_img - reconstructed_img) ** 2)


        mse = ssd_error / cropped_img.size
        rmse = np.sqrt(mse)
        nrmse = (rmse / 255.0) * 100
        print("NRMSE: {:.4f}%".format(nrmse))

        # (c) Compression Rate Calculation
        # codebook size = k * c^2 * 3 * 8 bits
        codebook_size_bits = k * (c**2) * channels * 8
        # index size = N * ceil(log2(k)) bits
        bits_per_index = math.ceil(math.log2(k))
        index_size_bits = N * bits_per_index
        compressed_size_bits = codebook_size_bits + index_size_bits

        compression_rate = compressed_size_bits / original_size_bits

        print(f"Results for c={c}, k={k}:")
        print(f"  - Reconstruction Error (SSD): {ssd_error:,.2f}")
        print(f"  - Codebook Size: {codebook_size_bits:,} bits")
        print(f"  - Index Size: {index_size_bits:,} bits")
        print(f"  - Compression Rate: {compression_rate:.6f} ({compression_rate * 100:.2f}%)")
        print("-" * 50)

