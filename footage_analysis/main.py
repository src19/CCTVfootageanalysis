import cv2
import numpy as np


def formatted_timestamp(cap):
  #gives the formatted timestamps for better readability
  timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)  
  minutes = int(timestamp_ms / (60 * 1000))  
  seconds = int((timestamp_ms % (60 * 1000)) / 1000) 
  milliseconds = int(timestamp_ms % 1000)  
  return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def process_video(video_path, output_path):
  """
  Takes a input video path from video_path checks for static frames frame by frame
  and then  compiles an output video with only those frames that are not static
  """

  cap = cv2.VideoCapture(video_path)

  if not cap.isOpened():
    print("Error: Couldn't open the video file.")
    return

  # Video properties
  frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  fps = cap.get(cv2.CAP_PROP_FPS)

  # Initialize video writer object (out) and last_mean
  out = None
  last_mean = 0

  while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('frame', frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # mean intensity difference of frames
    result = np.abs(np.mean(gray) - last_mean)
    last_mean = np.mean(gray)

  # Detects motion whenever the frame intensity difference falls below the given threshold 
    if result > 0.3: # This value can be adjusted for testing, higher the value the less sensitive it will be to frame changes
        print(f"Motion detected at: {formatted_timestamp(cap)}")
        if output_path:
            if not out:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
            out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  cap.release()
  if output_path:
    out.release()
  cv2.destroyAllWindows()


#write the required input output paths and then call the function process_video