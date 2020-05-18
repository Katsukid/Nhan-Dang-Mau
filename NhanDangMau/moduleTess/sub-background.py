import cv2
import numpy as np
import matplotlib.pyplot as plt
FOREGROUND_IMG = 'image2\\1.jpg'
BACKGROUND_IMG = 'image2\\bg.jpg'

def blur_color_img(img, kernel_width=5, kernel_height=5, sigma_x=2, sigma_y=2):
    img = np.copy(img) # we don't modify the original image
    img[:,:,0] = cv2.GaussianBlur(img[:,:,0], ksize=(kernel_width, kernel_height), sigmaX=sigma_x, sigmaY=sigma_y)
    img[:,:,1] = cv2.GaussianBlur(img[:,:,1], ksize=(kernel_width, kernel_height), sigmaX=sigma_x, sigmaY=sigma_y)
    img[:,:,2] = cv2.GaussianBlur(img[:,:,2], ksize=(kernel_width, kernel_height), sigmaX=sigma_x, sigmaY=sigma_y)
    return img   

def background_subtraction(fg_img, bg_img, diff_threshold=30):
    fg_img = blur_color_img(fg_img, 7, 7, 4, 4)
    bg_img = blur_color_img(bg_img, 7, 7, 4, 4)
    width = int(fg_img.shape[1])
    height = int(fg_img.shape[0])
    dim = (width, height)
    bg_img = cv2.resize(bg_img, dim)
    mask = fg_img - bg_img
    mask = np.abs(mask)
    mask = np.mean(mask, axis=2, keepdims=False)
    mask[mask<diff_threshold] = 0
    mask[mask>=diff_threshold] = 255
    mask = mask.astype(np.uint8)
    mask = cv2.medianBlur(mask, 7)
    return mask
    
def main(foreground_img, background_img):
    fg_img = cv2.imread(foreground_img) # [h, w, 3]
    bg_img = cv2.imread(background_img) # [h, w, 3]
    mask = background_subtraction(fg_img, bg_img)
    new_fg = np.zeros([fg_img.shape[0], fg_img.shape[1], 4]) # png image --> has 4-dims instead of 3-dims like color image
    new_fg[:,:,:3] = fg_img
    new_fg[:,:,3] = mask
    plt.figure()
    plt.subplot(2,2,1)
    plt.title('fg')
    plt.imshow(fg_img)
    plt.subplot(2,2,2)
    plt.title('Background')
    plt.imshow(bg_img)
    plt.subplot(2,2,3)
    plt.title('Mask')
    plt.imshow(mask)
    plt.subplot(2,2,4)
    plt.title('New')
    plt.imshow(new_fg)    
    plt.show()
    cv2.imwrite('mask.jpg', mask)
    cv2.imwrite('captain_america.png', new_fg)
    
if __name__ == "__main__":
    print('Running Background Subtraction for: %s and %s' % (FOREGROUND_IMG, BACKGROUND_IMG))
    main(foreground_img=FOREGROUND_IMG, background_img=BACKGROUND_IMG)



