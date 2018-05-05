import websocket
import time
import sys
import numpy as np
import cv2
import time
import threading


host = sys.argv[1]


def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Connection Close")

def on_open(ws):
    print('hi')
def on_open(ws):
    print("Connection Open")
    t = threading.Thread(target=capture)
    t.daemon = True
    t.start()


def capture():
    while(cap.isOpened()):           
        ret, frame = cap.read()
	_,imgEncode = cv2.imencode('.jpg',frame)
#     	print(imgEncode.tostring().encode("base64"))

        ws.send(imgEncode.tostring().encode("base64"))

        time.sleep(0.3)
    #ws.close()

if __name__ == "__main__":
    #websocket.enableTrace(True)
    cap = cv2.VideoCapture(0)

    while True:
        try:
            ws = websocket.WebSocketApp("ws://" + host + "/",
                                      on_message = on_message,
                                      on_error = on_error,
                                      on_close = on_close)
            ws.on_open = on_open
            ws.on_message = on_message
            ws.run_forever()
        except (KeyboardInterrupt, SystemExit):
            ws.close()
            cap.release()
            cv2.destroyAllWindows()
            raise
        except:
            ws.close()
            pass
