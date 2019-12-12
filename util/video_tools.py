import os
import cv2

""" Module that contains tools for handling videos
"""
def convert_images_to_video(
        resource_path, 
        video_name="video.avi", image_type="png", video_type="mp4v", fps=2.0):
    """ Function that converts a list of images to a video

    Args:
        resource_path(str): the path to the images and also where the video will be generated
        video_name(str): the name of the video
        video_type(str): the video type
        fps: the frame rate per second

    """

    images = [img for img in sorted(os.listdir(resource_path)) if img.endswith(image_type)]
    frame = cv2.imread(os.path.join(resource_path, images[0]))
    fourcc = cv2.VideoWriter_fourcc(*video_type)
    height, width, channels = frame.shape
    out = cv2.VideoWriter(
        os.path.join(resource_path, video_name), fourcc, fps, (width, height))

    for image in images:
        out.write(cv2.imread(os.path.join(resource_path, image)))
 
    out.release()
    cv2.destroyAllWindows()
    print("Generated video: " + os.path.join(resource_path, video_name))