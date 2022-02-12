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


#This function is to identify the color based,To get the color name, 
#we calculate a distance(d) which tells us how close we are to color and choose the one having minimum distance.
#Also as we have about 895 colors as a dataset in our csv the minimun is set to 900
#csv.loc determines the position to calculate the value of current R,G,B to the new R,G,B

def identify_the_color(R, G, B):
    minimum = 900
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            #Acessing color name
            cname = csv.loc[i, "color_name"]
    return cname


#This function is to trigger value as to at which position the click is made and produce x and y coordinates as to on image where the click is made define
#the red,green and blue values at those coordinates.

def action_by_mouse(event, x, y, flags, param):
    #When double click is made by left button of mouse only then the data i.e. the color is displayed as values are sent to the 
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global blue, green, red, x_coordinate, y_coordinate, action_clicked
        #As mouse is click the action is now true
        action_clicked = True
        x_coordinate = x
        y_coordinate = y
        blue, green, red = img[y, x]
        blue = int(blue)
        green = int(green)
        red = int(red)

#Naming the window that opens
cv2.namedWindow('Detecting colors in an image')
#Setting that if mouse is clicked double times then it should trigger the function action_by_mouse
cv2.setMouseCallback('Detecting colors in an image', action_by_mouse)

while(1):
    cv2.imshow("Detecting colors in an image", img)
    if action_clicked:
        
        #Box at which the text is appearing
        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (100, 100), (900, 60), (blue, green, red), -1)
        
        #Text getting displayed at the box
        # Creating text string to display( Color name and RGB values )
        text = identify_the_color(red, green, blue) + ' R=' + str(red) +' G=' + str(green) + ' B=' + str(blue)
        
        #How should the text appear in the box
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        #In computers, we define each color value within a range of 0 to 255
        cv2.putText(img, text, (50, 50), 2, 0.8,(255, 255, 255), 2, cv2.LINE_AA)
        
        #Setting action_clicked to false to find the name of the other color on which the mouse is clicked.
        action_clicked = False

    # Break the loop when one hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
