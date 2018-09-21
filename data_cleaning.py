import getopt
import glob
import sys
import os
import cv2
import numpy as np


def delete_frames():
    mydir = "data/frames"
    filelist = [f for f in os.listdir(mydir)]
    # print(filelist)
    for f in filelist:
        n = int(f.split('_')[2][:-4])
        if n % 4 != 0:
            # print(n)
            os.remove(os.path.join(mydir, f))


def get_videos(subject="*"):
    video_files = glob.glob("data/savee/AudioVisualClip/" + subject + "/*.avi")
    print(video_files)
    n = 0
    for video in video_files:
        temp = video.split("/")
        # print("asdf", (video, temp[3]))
        print(n)
        n = n + 1
        if n < 10:
            vid2frames(video, temp[3], temp[4][:-4])


def vid2frames(path="data/savee/AudioVisualClip/DC/a1.avi", subject="DC", vid_label="a1"):
    # noinspection PyArgumentList
    cap = cv2.VideoCapture(path)
    # print(cap)
    n = 0
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        # print(str(n) +"\r")
        if ret is True and n % 4 == 0:

            # Display the resulting frame
            # cv2.imshow('Frame', frame)
            cv2.imwrite('data/frames/' + subject + '_' + vid_label + '_' + str(n) + '.png', frame)
            n = n + 1
            # print(n)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


def translate_labels(l):
    label = []
    if 'a' == l:
        # Angry
        label = np.append(label, ([1, 0, 0, 0, 0, 0, 0]))
    elif 'd' == l:
        # Disgust
        label = np.append(label, ([0, 1, 0, 0, 0, 0, 0]))
    elif 'f' == l:
        # Fear
        label = np.append(label, ([0, 0, 1, 0, 0, 0, 0]))
    elif 'h' == l:
        # Happy
        label = np.append(label, ([0, 0, 0, 1, 0, 0, 0]))
    elif 'n' == l:
        # Neutral
        label = np.append(label, ([0, 0, 0, 0, 1, 0, 0]))
    elif 'sa' == l:
        # Sad
        label = np.append(label, ([0, 0, 0, 0, 0, 1, 0]))
    elif 'su' == l:
        # Surprise
        label = np.append(label, ([0, 0, 0, 0, 0, 0, 1]))
    return label


def numpy_array_image_label():
    files = glob.glob("data/frames/*.png")
    x_data = []
    label = []
    for myFile in files:
        temp = myFile.split("_")
        l: str = ''.join([i for i in temp[1] if not i.isdigit()])
        label.append(translate_labels(l))
        image = cv2.imread(myFile)
        x_data.append(image)

    images = np.array(x_data)
    labels = np.array(label)
    return images, labels


def to_numpy_array():
    image, label = numpy_array_image_label()
    image = np.copy(image)
    label = np.copy(label)
    print("image", image.shape)
    print("label", label.shape)
    np.save('data/x_train', image)
    np.save('data/y_train', label)


def main(argv):
    global opts
    help_text = """data_cleaning.py  -h --help
    -h --help       Get help.
    -s --subject    Specify subject name[JK,DC,...]
    -d --delete     Delete every frame other than multiples of 4.
    -n --numpy      Save data/frames/ content as a numpy array in data/x_train.npy and data/y_train.npy
    """
    try:
        opts, args = getopt.getopt(argv, "hs:dn")
    except getopt.GetoptError:
        print(help_text)
        sys.exit()
    subject = "*"
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_text)
            sys.exit()
        elif opt in ('-s', '--subject'):
            subject = str(arg)
            get_videos(subject)
            sys.exit()
        elif opt in ('-d', '--delete'):
            delete_frames()
            sys.exit()
        elif opt in ('-n', '--numpy'):
            to_numpy_array()
            sys.exit()
    print(help_text)


if __name__ == "__main__":
    # sys.stdout = open('logs/cleaning.txt', 'w')
    # sys.stderr = open('logs/cleaning-err.txt', 'w')
    main(sys.argv[1:])
