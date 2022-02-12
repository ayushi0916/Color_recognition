import numpy as np
import pandas as pd
import cv2

#Reading image using open cv library cv2
img = cv2.imread('colorfulimage.jpg')

#Defining the index to be used as the column titles in the csv
index = ["color", "color_name", "hex", "R", "G", "B"]

#Reading the csv to determine the colors based on their RGB values.
csv = pd.read_csv('list_of_colors.csv', names=index, header=None)

# Initially we are setting the action to false, as not mouse action is done
action_clicked = False

#Defining the colors and coordinates and setting them to zero
red = green = blue = x_coordinate = y_coordinate = 0


def identify_the_color(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname



def action_by_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global blue, green, red, x_coordinate, y_coordinate, action_clicked
        action_clicked = True
        x_coordinate = x
        y_coordinate = y
        blue, green, red = img[y, x]
        blue = int(blue)
        green = int(green)
        red = int(red)


cv2.namedWindow('Detecting colors in an image')
cv2.setMouseCallback('Detecting colors in an image', action_by_mouse)

while(1):
    cv2.imshow("Detecting colors in an image", img)
    if action_clicked:

        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (30, 30), (900, 60), (blue, green, red), -1)
        
        # Creating text string to display( Color name and RGB values )
        text = identify_the_color(red, green, blue) + ' R=' + str(red) +' G=' + str(green) + ' B=' + str(blue)

        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8,(255, 255, 255), 2, cv2.LINE_AA)
        
        # For very light colours we will display text in black colour
        if(red+green+blue >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        action_clicked = False

    # Break the loop when one hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
