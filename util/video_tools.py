import os
import cv2

def convert_images_to_video(
        resource_path, 
        video_name="video.avi", image_type="png", video_type="mp4v"):
    images = [img for img in sorted(os.listdir(resource_path)) if img.endswith(image_type)]
    frame = cv2.imread(os.path.join(resource_path, images[0]))
    fourcc = cv2.VideoWriter_fourcc(*video_type)
    height, width, channels = frame.shape
    out = cv2.VideoWriter(
        os.path.join(resource_path, video_name), fourcc, 2.0, (width, height))

    for image in images:
        out.write(cv2.imread(os.path.join(resource_path, image)))
 
    out.release()
    cv2.destroyAllWindows()
    print("Generated video: " + os.path.join(resource_path, video_name))