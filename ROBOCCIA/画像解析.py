import time
import numpy as np
import cv2


def Clahe(img_name): #ヒストグラム平坦化
    img = cv2.imread(img_name) # 画像を読み込む

    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV) # RGB => YUV(YCbCr)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) # claheオブジェクトを生成
    img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0]) # 輝度にのみヒストグラム平坦化
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR) # YUV => RGB
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # RGBからHSVに変換

    #色の範囲を指定
    LOW_red1 = np.array([0, 50, 50]) # 各最小値を指定
    HIGH_red1 = np.array([14, 255, 255]) # 各最大値を指定
    LOW_red2 = np.array([165, 50, 50])
    HIGH_red2 = np.array([179, 255, 255])
    LOW_blue = np.array([87, 50, 50])
    HIGH_blue = np.array([116, 255, 255])
    LOW_white = np.array([0, 0, 200])
    HIGH_white = np.array([179, 25, 255])
    #LOW_black = np.array([0, 0, 0])
    #HIGH_black = np.array([180, 255, 20])

    bin_red1 = cv2.inRange(hsv, LOW_red1, HIGH_red1) # マスクを作成
    bin_red2 = cv2.inRange(hsv, LOW_red2, HIGH_red2)
    bin_blue = cv2.inRange(hsv, LOW_blue, HIGH_blue)
    bin_white = cv2.inRange(hsv, LOW_white, HIGH_white)

    mask_red = bin_red1 + bin_red2 # 必要ならマスクを足し合わせる
    mask_blue = bin_blue
    mask_white = bin_white
    masked_red= cv2.bitwise_and(img, img, mask= mask_red) # 元画像から特定の色を抽出
    masked_blue= cv2.bitwise_and(img, img, mask= mask_blue)
    masked_white= cv2.bitwise_and(img, img, mask= mask_white)
    cv2.imwrite("out_img_red.jpg", masked_red) # 書き出す
    cv2.imwrite("out_img_blue.jpg", masked_blue)
    cv2.imwrite("out_img_white.jpg", masked_white)


def Circle(color):
    img = cv2.imread('out_img_'+color+'.jpg')
    cv2.imwrite('out_img_'+color+'_hough.jpg',img)
    img_raw = cv2.imread('out_img_'+color+'_hough.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=250,param2=11,minRadius=30,maxRadius=50)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(img_raw,(i[0],i[1]),i[2]+5,(0,255,0),2)
            cv2.circle(img_raw,(i[0],i[1]),2,(0,0,255),1)
    cv2.imwrite('circles_'+color+'.jpg',img_raw)


def main():
    cap = cv2.VideoCapture(1) #1なら外部カメラ。0なら内蔵カメラ。（大岡環境の場合）
    fps = int(cap.get(cv2.CAP_PROP_FPS)) #動画のFPSを取得

    #カメラから映像を取得し続けるループ
    while True:
        ret, frame = cap.read() #カメラから画像を取得

        #繰り返し分から抜けるためのif文
        key =cv2.waitKey(10)
        if key == 27:
            break

        #ｒが押されたときに画像を出力
        key =cv2.waitKey(10)
        if key == ord("r"):
            filename = "img_out.png"
            cv2.imwrite(filename, frame)
            Clahe(filename)
            Circle('red')
            Circle('blue')
            Circle('white')

        #ウィンドウでの再生速度を元動画と合わせる
        time.sleep(1/fps)
        # ウィンドウで表示
        cv2.imshow('target_frame', frame)

    cap.release() #メモリを解放
    cv2.destroyAllWindows() # ウィンドウを破棄


if __name__ == "__main__":
    main()