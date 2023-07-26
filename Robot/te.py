import cv2

vid_cap = cv2.VideoCapture("R.mkv")

# store every frame from video file
success, image = vid_cap.read()
count = 0
frames = []

while vid_cap.isOpened():
    success, image = vid_cap.read()
    if success:
        img = cv2.resize(image, (512, 512))
        frames.append(img)
        count += 1
    else:
        break

vid_cap.release()