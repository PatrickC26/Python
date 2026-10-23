import math
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def compress_image_kmeans(img):
    img_arr = np.array(img, dtype=np.float64)
    orig_h, orig_w, channels = img_arr.shape

    k_values = [6, 10, 14]
    c_values = [20, 50, 80]

    for c in c_values:
        # Crop borders to the nearest multiple of c for non-overlapping windows
        h = (orig_h // c) * c
        w = (orig_w // c) * c
        cropped_img = img_arr[:h, :w, :]

        num_blocks_h = h // c
        num_blocks_w = w // c
        N = num_blocks_h * num_blocks_w

        # Extract non-overlapping c x c windows and flatten each in Fortran ('F') order
        windows = []
        for i in range(num_blocks_h):
            for j in range(num_blocks_w):
                window = cropped_img[i * c : (i + 1) * c, j * c : (j + 1) * c, :]
                windows.append(window.flatten(order="F"))

        X = np.array(windows)  # Shape: (N, c * c * 3)

        # Baseline original size in bits
        original_size_bits = h * w * channels * 8

        for k in k_values:
            print(f"Running k-means for c={c}, k={k} (N={N} windows)...")

            # Fit k-means clustering
            kmeans = KMeans(n_clusters=k)
            # kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X)

            # Codebook reference vectors directly given by cluster_centers_
            codebook = kmeans.cluster_centers_  # Shape: (k, c * c * channels)

            # Map cluster labels to reconstructed window vectors
            reconstructed_windows = codebook[labels]

            # Reconstruct 2D image from flattened vectors
            reconstructed_img = np.zeros((h, w, channels), dtype=np.float64)
            window_idx = 0
            for i in range(num_blocks_h):
                for j in range(num_blocks_w):
                    window_vec = reconstructed_windows[window_idx]
                    reconstructed_img[
                        i * c : (i + 1) * c, j * c : (j + 1) * c, :
                    ] = window_vec.reshape((c, c, channels), order="F")
                    window_idx += 1

            # (a) Round, clip to [0, 255], and convert to integer before saving
            reconstructed_uint8 = np.clip(
                np.round(reconstructed_img), 0, 255
            ).astype(np.uint8)
            output_filename = f"HW2_1-3/HW2_1-3_2_coffee_c{c}_k{k}.png"
            Image.fromarray(reconstructed_uint8).save(output_filename)

            # (b) Reconstruction Error: Sum of Squared Differences (SSD)
            reconstruction_error = np.sum((cropped_img - reconstructed_img) ** 2)

            # (c) Compression Rate Calculation
            # codebook size = k * c^2 * 3 * 8 bits
            codebook_size = k * (c**2) * channels * 8
            # index size = N * ceil(log2(k)) bits
            index_size = N * math.ceil(math.log2(k))
            compressed_size = codebook_size + index_size
            compression_rate = compressed_size / original_size_bits

            print(f"Results for c={c}, k={k}:")
            print(f"  - Output Image File: {output_filename}")
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
    compress_image_kmeans(data.coffee())