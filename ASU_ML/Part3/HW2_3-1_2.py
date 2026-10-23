import os
import sys
import torch
import cv2
import matplotlib.pyplot as plt

def run_object_detection(image_path="Assignment 2_image.jpg", weights_path="yolov7.pt", conf_thresh=0.25):
    """
    Run object detection on an image using YOLOv7.

    Args:
        image_path (str): Path to input image file.
        weights_path (str): Path to YOLOv7 pretrained weights.
        conf_thresh (float): Minimum confidence threshold for detections.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Weights file not found: {weights_path}")

    print(f"[INFO] Loading YOLOv7 model from '{weights_path}'...")
    # Load model using torch.hub from local repository
    model = torch.hub.load('./yolov7', 'custom', path_or_model=weights_path, source='local')
    model.conf = conf_thresh  # Set confidence threshold

    print(f"[INFO] Running object detection on '{image_path}'...")
    results = model(image_path)

    # 1. Print detection summary
    print("\n--- Detection Summary ---")
    results.print()

    # 2. Extract bounding boxes and details as pandas DataFrame
    detections = results.pandas().xyxy[0]
    print("\n--- Detailed Detections ---")
    if len(detections) == 0:
        print("No objects detected above the confidence threshold.")
    else:
        for idx, row in detections.iterrows():
            print(f"[{idx + 1}] Class: {row['name']} | Confidence: {row['confidence']:.2%} | Box: [{row['xmin']:.1f}, {row['ymin']:.1f}, {row['xmax']:.1f}, {row['ymax']:.1f}]")

    # 3. Save the annotated image
    output_filename = "HW2_3-1_2_result.jpg"
    # results.render() annotates the image in-place (RGB format)
    rendered_images = results.render()
    annotated_img_rgb = rendered_images[0]
    
    # Convert RGB to BGR for OpenCV saving
    annotated_img_bgr = cv2.cvtColor(annotated_img_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_filename, annotated_img_bgr)
    print(f"\n[INFO] Annotated output saved to: '{output_filename}'")

    return results, detections

if __name__ == "__main__":
    # Allow passing custom image path as CLI argument if provided
    img_path = sys.argv[1] if len(sys.argv) > 1 else "Assignment 2_image.jpg"
    run_object_detection(image_path=img_path)
