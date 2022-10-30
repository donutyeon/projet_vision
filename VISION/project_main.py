import cv2
from project_tests import encode, decode, show_image


input_image = "VISION\supernova.jpg"
output_image = "encoded_image.PNG"
secret_data = "This is a top secret message."
im = cv2.imread("encoded_image.PNG",-1)
#cv2.imshow("a",im)
# encode the data into the image
encoded_image = encode(image_name=input_image, secret_data=secret_data)
# save the output image (encoded image)
cv2.imwrite(output_image, encoded_image)

#show_image(output_image)

# decode the secret data from the image
decoded_data = decode(output_image)
print("[+] Decoded data:", decoded_data)
cv2.waitKey(0)
cv2.destroyAllWindows()

