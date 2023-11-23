import cv2 as cv
import numpy as np
import pyautogui

def press_to(sub_image_location):
    img_rgb = pyautogui.screenshot()
    img_rgb = np.array(img_rgb)
    assert img_rgb is not None, "File could not be read, check with os.path.exists()"
    
    # Convert screenshot to a different color space if needed
    # For example, convert to HSV color space
    img_hsv = cv.cvtColor(img_rgb, cv.COLOR_BGR2HSV)
    # Extract the value (brightness) channel
    img_value = img_hsv[:, :, 2]

    template = cv.imread(sub_image_location)
    assert template is not None, "File could not be read, check with os.path.exists()"
    
    # Apply color transformation to the template image
    # For example, convert to grayscale
    template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    
    # Define the scales you want to use for template matching
    scales = [1.0]  # You can adjust these scales as needed
    
    found = False
    threshold = 0.8
    for scale in scales:
        resized_template = cv.resize(template_gray, None, fx=scale, fy=scale)
        w, h = resized_template.shape[::-1]
        
        res = cv.matchTemplate(img_value, resized_template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        
        if len(loc[0]) > 0:
            found = True
            # Iterate over all matching locations at the current scale
            for pt in zip(*loc[::-1]):
                cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                center_x = int((pt[0] + pt[0] + w) / 2)
                center_y = int((pt[1] + pt[1] + h) / 2)
                
                # Click on the center coordinates of the detected area
                pyautogui.click(center_x, center_y)
        
    if found:
        # Save the image with drawn rectangles
      cv.imwrite(f"result image of {sub_image_location}.png", img_rgb)
    
    if not found:
        return False
    
    return True

