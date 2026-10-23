import math
import numpy as np
from PIL import Image
from sklearn.cluster import AgglomerativeClustering


def compress_image_hierarchical(img):
    img_arr = np.array(img, dtype=np.float64)
    orig_h, orig_w, channels = img_arr.shape

    k_values = [6, 10, 14]
    c_values = [20, 50, 80]

    for c in c_values:
        # Crop borders so height and width divide evenly into c x c windows
        h = (orig_h // c) * c
        w = (orig_w // c) * c
        cropped_img = img_arr[:h, :w, :]

        num_blocks_h = h // c
        num_blocks_w = w // c
        N = num_blocks_h * num_blocks_w  # Total number of non-overlapping windows

        # Extract non-overlapping c x c windows and flatten each using Fortran order
        windows = []
        for i in range(num_blocks_h):
            for j in range(num_blocks_w):
                window = cropped_img[i * c : (i + 1) * c, j * c : (j + 1) * c, :]
                windows.append(window.flatten(order="F"))

        X = np.array(windows)  # Shape: (N, c * c * 3)

        # Baseline original size in bits
        original_size_bits = h * w * channels * 8

        for k in k_values:
            print(f"Clustering for c = {c}, k = {k} (N = {N} windows)...")

            # Agglomerative hierarchical clustering with single linkage
            clustering = AgglomerativeClustering(
                n_clusters=k, linkage="single", metric="euclidean"
            )
            labels = clustering.fit_predict(X)

            # Compute reference vectors (cluster centers/centroids)
            feature_dim = c * c * channels
            codebook = np.zeros((k, feature_dim), dtype=np.float64)
            for cluster_idx in range(k):
                members = X[labels == cluster_idx]
                if len(members) > 0:
                    codebook[cluster_idx] = np.mean(members, axis=0)
                else:
                    codebook[cluster_idx] = np.zeros(feature_dim)

            # Reconstruct window vectors by mapping cluster labels back to codebook vectors
            reconstructed_windows = codebook[labels]

            # Reconstruct full image array
            reconstructed_img = np.zeros((h, w, channels), dtype=np.float64)
            window_idx = 0
            for i in range(num_blocks_h):
                for j in range(num_blocks_w):
                    window_vec = reconstructed_windows[window_idx]
                    reconstructed_img[
                        i * c : (i + 1) * c, j * c : (j + 1) * c, :
                    ] = window_vec.reshape((c, c, channels), order="F")
                    window_idx += 1

            # Keep pixel values as integers (int) before visualization/saving
            reconstructed_int = np.clip(np.round(reconstructed_img), 0, 255).astype(
                np.uint8
            )

            # (a) Save the compressed/reconstructed image
            out_filename = f"HW2_1-1/HW2_1-1_2-coffee_c{c}_k{k}.png"
            Image.fromarray(reconstructed_int).save(out_filename)

            # (b) Reconstruction Error: Sum of Squared Differences (SSD)
            reconstruction_error = np.sum((cropped_img - reconstructed_img) ** 2)

            # (c) Compression Rate Calculation
            # codebook size = k * c^2 * 3 * 8 bits
            codebook_size = k * (c**2) * channels * 8
            # index size = N * ceil(log2(k)) bits
            index_size = N * math.ceil(math.log2(k))
            compressed_size = codebook_size + index_size
            compression_rate = compressed_size / original_size_bits

            # Print outputs
            print(f"Results for c = {c}, k = {k}:")
            print(f"  - Output Image File: {out_filename}")
            print(f"  - Reconstruction Error (SSD): {reconstruction_error:,.2f}")
            print(f"  - Codebook Size: {codebook_size:,} bits")
            print(f"  - Index Size: {index_size:,} bits")
            print(f"  - Compressed Size: {compressed_size:,} bits")
            print(f"  - Original Size: {original_size_bits:,} bits")
            print(f"  - Compression Rate: {compression_rate:.6f} ({compression_rate * 100:.2f}%)")
            print("-" * 50)

from skimage import data
if __name__ == "__main__":
    # Point this to your target image file
    compress_image_hierarchical(data.coffee())