from pydoc import plain
from PIL import Image


def decryption(img):
    # This function will extract the hidden encoded message from the image and decode it 
    image = Image.open(img, 'r')
    plainText = ''
    imageData = iter(image.getdata())
    while True:
        pixels = [value for value in imageData.__next__()[:3] + imageData.__next__()[:3] + imageData.__next__()[:3]]
        binaryFormatString = ''
        # odd RGB value means 0, even RGB value means 1
        for i in pixels[:8]:
            if i % 2 != 0:
                binaryFormatString += '0'
            else:
                binaryFormatString += '1'
        plainText += chr(int(binaryFormatString, 2))
        # when the 9th pixel is odd, decode end
        if pixels[-1] % 2 != 0:
            print("The encoded message is: " + plainText)
            break
    

def main():
    img = "encrypted_image.png"
    decryption(img)

if __name__=="__main__":
    main()