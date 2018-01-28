import cv2
import sys
import os
 
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
    # BOOSTING, KCF, TLD, MEDIANFLOW or GOTURN
     
    tracker = cv2.Tracker_create("KCF") # tracker: KCF
 
    # Read video
    video = cv2.VideoCapture("drake2.mp4") #input image path
 
    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
     
    # Define an initial bounding box
    #bbox = (287, 23, 86, 320)
 
    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)

    #rescale bounding box due to difference in frame dimension/resolution
    #scale subjected to changes
    
    #xscale = 1920/1280
    #yscale = 1080/720

    #bbox_list = [bbox[0]*xscale, bbox[1]*yscale, bbox[2]*xscale, bbox[3]*yscale]

    #bbox = tuple(bbox_list) 
 
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
 
    # Return bounding box info to a file
    working_path = "/home/meiyi/track" # path for the file generated

    if not os.path.exists(os.path.join(working_path,'drake.txt')):
        with open(os.path.join(working_path,'annotation.txt'),'w') as annotation_file:
            annotation_file.write("\n")

    frame_index = 1
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Update tracker
        ok, bbox = tracker.update(frame)
        
        # Append the new bounding box
        with open(os.path.join(working_path,'annotation.txt'),'a') as a_file:
            a_file.write(" ".join(["frame"+str(frame_index),' '.join([str(bbox[0]), str(bbox[1]), str(bbox[2]), str(bbox[3])]), '\n']))
        frame_index += 1

        # Draw bounding box
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))  #tuple for starting point
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))   #tuple for end point
            cv2.rectangle(frame, p1, p2, (0,0,255))
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
