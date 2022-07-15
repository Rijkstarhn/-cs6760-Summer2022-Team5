from PIL import Image
import os


# encode msg
# to be done

# encode img
def processImage(pixels, data):
    # This function will convert the encoded message from ascii binary form into pixels
    # For example, H = 01001000, we will use 3 pixels(3*3 RBG value) to
    # store the 8 bits. We define odd RBG value corresponds to 0, even RBG value to 1.
    # Let's say the original R value of the first pixel is 18, then we need to increase it
    # to 19 because 19 is an odd value which corresponds to 0.
    # We also need to set each 9th pixel value to even value. By doing that, as long as we
    # set the 9th pixel value of last character to odd, we know this is the end of the msg. 
    binaryFormMsg = []
    for i in data:
        binary_data = format(ord(i), '08b') # generate the corresponding ascii code for the data
        binaryFormMsg.append(binary_data)
    lengthOfMsg = len(binaryFormMsg)
    imageData = iter(pixels)
    for idx in range(lengthOfMsg):
        pixels = [val for val in imageData.__next__()[:3] + imageData.__next__()[:3] + imageData.__next__()[:3]]
        for bit in range(8):
            if (binaryFormMsg[idx][bit] == '1') and (pixels[bit] % 2 != 0):
                pixels[bit] -= 1
            elif (binaryFormMsg[idx][bit] == '0') and (pixels[bit] % 2 == 0):
                if pixels[bit] == 0:
                    pixels[bit] += 1
                pixels[bit] -= 1
        bit = 8
        if pixels[bit] % 2 != 0:
            pixels[bit] += 1
            pixels[bit] %= 255
        if idx == (lengthOfMsg-1):
            if pixels[-1] % 2 == 0:
                if pixels[-1] == 0:
                    pixels[-1] += 1
                else:
                    pixels[-1] -= 1
        pixels = tuple(pixels)
        print(pixels)
        yield pixels[:3]
        yield pixels[3:6]
        yield pixels[6:9]

def updateImagePixel(img, data):
    # This method will encode data to the new image that will be created
    size = img.size[0]
    (col, row) = (0, 0)
    for pixel in processImage(img.getdata(), data):
        img.putpixel((col, row), pixel)
        if size-1 == col:
            col = 0; row += 1
        else:
            col += 1

def encryption(img, text):
    # This function will encode the msg and hide it into the image.
    # Then generate an encrypted image called "encrypted_image.png".
    image = Image.open(img, 'r')
    if (len(text) == 0):
        print("No message inputed!")
        return
    if (len(img) == 0):
        print("No image inputed!")
        return
    # output the encoded img
    newImage = image.copy()
    updateImagePixel(newImage, text)
    newImageName = 'encrypted_image.png'
    newImage.save(newImageName, 'png')
    print("encrypted image path:" + os.path.abspath("encrypted_image.png"))


def main():
    text = "Hello World"
    img = "vancouver1.jpg"
    encryption(img, text)

if __name__=="__main__":
    main()



