import cv2
import numpy as np

import math

import datetime
import time
import os
import sys

import scanDir as clnfilss

vdoRoot = 'recode'


def creatNewFilename():
    insNow = datetime.datetime.now()
    savedir = vdoRoot + '/' + str(insNow.strftime('%Y%m%d')) + '/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)

    saveVdo = savedir +       \
        str(insNow.strftime('%Y%m%d_%H%M%S')) + '.mp4'
    return saveVdo


def getCameraFps(index):
    # by default
    outFps = 12.0
    if index == 0:
        # by system

        video = cv2.VideoCapture(0)
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

        if int(major_ver) < 3:
            fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
            print(
                "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
        else:
            fps = video.get(cv2.CAP_PROP_FPS)
            print(
                "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

        video.release()
        cv2.destroyAllWindows()
        outFps = fps

    elif index == 1:
        # by testing

        video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        #num_frames = 2*3*5*7
        num_frames = 240

        count = 0
        start = time.time()

        while(video.isOpened() and count < num_frames):
            count = count + 1
            tmppss = video.read()

        end = time.time()

        fps = count / (end-start)
        print("******Estimated frames per second : {0} ******".format(fps))

        # Release video
        video.release()
        cv2.destroyAllWindows()
        outFps = math.floor(fps*10)/10

    else:
        # by user
        outFps = 24.0

    return outFps


def main():
    fpss = getCameraFps(-1)

    # =========================================================
    width = 1280
    height = 720

    boxRate = 0.001
    # min moving box
    moveArea = math.ceil(width * height * boxRate)

    maxVideoLengthMinut = 30
    wattingMinut = 5

    sNowDaytime = datetime.datetime.now()
    endrecordTime = sNowDaytime + datetime.timedelta(minutes=-5)
    maxVdoLenTime = sNowDaytime + datetime.timedelta(minutes=-5)

    cleanfile = True

    # =========================================================
    # blur ksize
    ksize = (4, 4)

    # open close kernel
    kernel = np.ones((5, 5), np.uint8)

    # =========================================================
    # 開啟網路攝影機
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # mp4
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')

    # 設定擷取影像的尺寸大小
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    #outVdo = cv2.VideoWriter(creatNewFilename(), fourcc, fpss, (width, height))

    # 初始化平均影像
    ret, frame = cap.read()
    avg = cv2.blur(frame, ksize)
    avg_float = np.float32(avg)

    # =========================================================
    while(cap.isOpened()):
        # 讀取一幅影格
        ret, frame = cap.read()

        # 模糊處理
        blur = cv2.blur(frame, ksize)

        # 計算目前影格與平均影像的差異值
        diff = cv2.absdiff(avg, blur)

        # 將圖片轉為灰階
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # 篩選出變動程度大於門檻值的區域
        ret, thresh = cv2.threshold(gray, 16, 255, cv2.THRESH_BINARY)

        # 使用型態轉換函數去除雜訊
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        thresh = cv2.morphologyEx(
            thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        # cv.findContours
        # contours, hierarchy = cv.findContours(image, mode, method[, contours[, hierarchy[, offset]]])
        # 產生等高線
        cnts, cntImg = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            # 忽略太小的區域
            if cv2.contourArea(c) >= moveArea:
                endrecordTime = datetime.datetime.now() + datetime.timedelta(minutes=wattingMinut)
                # 計算等高線的外框範圍
                (x, y, w, h) = cv2.boundingRect(c)
                # 畫出外框
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        insNow = datetime.datetime.now()
        if(endrecordTime > insNow):
            if(maxVdoLenTime < insNow):
                maxVdoLenTime = insNow +       \
                    datetime.timedelta(minutes=maxVideoLengthMinut)
                outVdo = cv2.VideoWriter(
                    creatNewFilename(), fourcc, fpss, (width, height))

            outVdo.write(frame)

        # 畫出等高線（除錯用）
        cv2.drawContours(frame, cnts, -1, (0, 255, 255), 2)

        # 顯示偵測結果影像
        cv2.imshow('saveVdo', frame)

        if int(round(insNow.second)) == int(round(0.0)) and cleanfile == True:
            clnfilss.scanDir(vdoRoot)
            # print(insNow)
            # print(insNow.microsecond)
            cleanfile = False
        elif int(round(insNow.second)) == int(round(1.0)):
            cleanfile = True

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 更新平均影像
        cv2.accumulateWeighted(blur, avg_float, 0.01)
        avg = cv2.convertScaleAbs(avg_float)

    # ==========================================================
    cap.release()
    outVdo.release()
    cv2.destroyAllWindows()

    return 0


if __name__ == '__main__':
    main()
