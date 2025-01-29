import cv2
# Research cv2

input = cv2.VideoCapture( 1 )


while True:   
    ret, frame = input.read()
    if ret:   
        cv2.imshow( "video output", frame )

    key = cv2.waitKey(1) & 0xFF
    if  key == ord( 'x' ):   
        break
    if key == ord('z'):
        focus = 0  # min: 0, max: 255, increment:5
        input.set(28, focus)

input.release()   
cv2.destroyAllWindows()



def show_webcam(mirror=False):
            scale=10

            cam = cv2.VideoCapture(0)
            while True:
                ret_val, image = cam.read()
                if mirror: 
                    image = cv2.flip(image, 1)


                #get the webcam size
                height, width, channels = image.shape

                #prepare the crop
                centerX,centerY=int(height/2),int(width/2)
                radiusX,radiusY= int(scale*height/100),int(scale*width/100)

                minX,maxX=centerX-radiusX,centerX+radiusX
                minY,maxY=centerY-radiusY,centerY+radiusY

                cropped = image[minX:maxX, minY:maxY]
                resized_cropped = cv2.resize(cropped, (width, height)) 

                cv2.imshow('my webcam', resized_cropped)
                if cv2.waitKey(1) == 27: 
                    break  # esc to quit

                #add + or - 5 % to zoom

                if cv2.waitKey(1) == 0: 
                    scale += 5  # +5

                if cv2.waitKey(1) == 1: 
                    scale = 5  # +5

            cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()