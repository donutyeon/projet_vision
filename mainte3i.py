import cv2
from restarting import encode,decode


input_image = "jsp.jpeg"
output_image = "encoded_image.png"
secret_data = "rania"
for letter in secret_data:
    print(ord(letter))

print(chr(int('00001101',2)))
#im = cv2.imread("encoded_image.PNG",-1)
#cv2.imshow("a",im)
# encode the data into the image
encoded_image = encode(img=input_image, message=secret_data)
# save the output image (encoded image)
cv2.imwrite(output_image, encoded_image)

# decode the secret data from the image
decoded_data = decode(output_image)
print("[+] Decoded data:", decoded_data)
cv2.waitKey(0)
cv2.destroyAllWindows()

