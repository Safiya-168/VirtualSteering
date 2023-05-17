import math # for mathematical function
import keyinput # for key inputs defined in the other file
import cv2
import mediapipe as mp

cap=cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
with mp_hands.Hands() as hands:
    while True:
        rt,video=cap.read()
        video = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
        results = hands.process(video)
        video=cv2.cvtColor(video,cv2.COLOR_RGB2BGR)
        font=cv2.FONT_HERSHEY_DUPLEX
        videoHeight, videoWidth, _ = video.shape
        co=[]
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    video,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS)
                for point in mp_hands.HandLandmark:
                    if str(point) == "HandLandmark.WRIST":
                      normalizedLandmark = hand_landmarks.landmark[point]
                      pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                        normalizedLandmark.y,
                                                                                    videoWidth, videoHeight)

                      try:
                        co.append(list(pixelCoordinatesLandmark))
                      except:
                          continue

        if len(co) == 2:
            xm, ym = (co[0][0] + co[1][0]) / 2, (co[0][1] + co[1][1]) / 2
            radius = 150
            try:
                m=(co[1][1]-co[0][1])/(co[1][0]-co[0][0])
            except:
                continue
            a = 1 + m ** 2
            b = -2 * xm - 2 * co[0][0] * (m ** 2) + 2 * m * co[0][1] - 2 * m * ym
            c = xm ** 2 + (m ** 2) * (co[0][0] ** 2) + co[0][1] ** 2 + ym ** 2 - 2 * co[0][1] * ym - 2 * co[0][1] * co[0][
                0] * m + 2 * m * ym * co[0][0] - 22500
            xa = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
            xb = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
            ya = m * (xa - co[0][0]) + co[0][1]
            yb = m * (xb - co[0][0]) + co[0][1]
            if m!=0:
                ap = 1 + ((-1/m) ** 2)
                bp = -2 * xm - 2 * xm * ((-1/m) ** 2) + 2 * (-1/m) * ym - 2 * (-1/m) * ym
                cp = xm ** 2 + ((-1/m) ** 2) * (xm ** 2) + ym ** 2 + ym ** 2 - 2 * ym * ym - 2 * ym * xm * (-1/m) + 2 * (-1/m) * ym * xm - 22500
                try:
                    xap = (-bp + (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
                    xbp = (-bp - (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
                    yap = (-1 / m) * (xap - xm) + ym
                    ybp = (-1 / m) * (xbp - xm) + ym

                except:
                    continue

            cv2.circle(video,(int(xm), int(ym)),radius, (195, 255, 62), 15)
            cv2.line(video, (int(xa), int(ya)), (int(xb), int(yb)), (195, 255, 62), 20)
            if co[0][0] > co[1][0] and co[0][1]>co[1][1] and co[0][1] - co[1][1] > 65:
                print("Turn left.")
                keyinput.press_key('a')
                cv2.putText(video, "Turn left", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(video, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)

            elif co[1][0] > co[0][0] and co[1][1]> co[0][1] and co[1][1] - co[0][1] > 65:
                print("Turn left.")
                keyinput.press_key('a')
                cv2.putText(video, "Turn left", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(video, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)


            elif co[0][0] > co[1][0] and co[1][1]> co[0][1] and co[1][1] - co[0][1] > 65:
                print("Turn right.")
                keyinput.press_key('d')
                cv2.putText(video, "Turn right", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(video, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)

            elif co[1][0] > co[0][0] and co[0][1]> co[1][1] and co[0][1] - co[1][1] > 65:
                print("Turn right.")
                keyinput.press_key('d')
                cv2.putText(video, "Turn right", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(video, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)
            
            else:
                print("keeping straight")
                keyinput.press_key('w')
                cv2.putText(video, "keep straight", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                if ybp>yap:
                    cv2.line(video, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)
                else:
                    cv2.line(video, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)
        if len(co)==1:
            print("keeping back")
            keyinput.press_key('s')
            cv2.putText(video, "keeping back", (50, 50), font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('MediaPipe Hands', cv2.flip(video, 1))
        if cv2.waitKey(1)==ord('q'):
            break
    cap.release()