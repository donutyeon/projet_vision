import cv2
import numpy as np

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "016b") for i in data ])
    elif isinstance(data, bytes):
        return ''.join([ format(i, "016b") for i in data ])
    elif isinstance(data, np.ndarray):
        return [ format(i, "016b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint16):
        return format(data, "016b")
    else:
        raise TypeError("Type not supported.")


def encode(image_name, secret_data):
    # read the image
    image = cv2.imread(image_name)
    # maximum bytes to encode
    image_16 = np.array(image, dtype = np.uint16)
    image_16 *= 256
    #image_rgb = cv2.cvtColor(image_16, cv2.COLOR_RGB2BGR)
    #cv2.imshow("im",image_16)
    image_rgb = cv2.cvtColor(image_16, cv2.COLOR_BGR2YCrCb)
    
    #n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    n_bytes_test = image_rgb.shape[0] * image.shape[1] * 3 // 16
    print((n_bytes_test))
    print("[*] Maximum bytes to encode:", n_bytes_test)
    if len(secret_data) > n_bytes_test:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    print(binary_secret_data)
    data_len = len(binary_secret_data)
    for row in image_rgb:
        for pixel in row:
            # convert YCrCb values to binary format
            Y, Cr, Cb = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
        #     if data_index < data_len:
        #         # least significant red pixel bit
        #         pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
        #         data_index += 1
            # if data_index < data_len:
            #     # least significant green pixel bit
            #     pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
            #     data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(Cb[:-1] + binary_secret_data[data_index], 2)
                # sum = bin(add(int(Cb[:-1],2),int(binary_secret_data[data_index],2)))
                # print(sum[2:])
                # pixel[2] = sum[2:]
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_YCrCb2BGR)
    #image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB)
    
    return image_rgb


def decode(image_name):
    print("[+] Decoding...")
    # read the image
    print(image_name)
    image = cv2.imread(image_name,-1)
    cv2.imshow("im",image)
    #image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #cv2.imshow("im",image_rgb)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    print(image_rgb.dtype)
    binary_data = ""
    for row in image_rgb:
        for pixel in row:
            Y, Cr, Cb = to_bin(pixel)
            #binary_data += Y[-1]
            #binary_data += Cr[-1]
            binary_data += Cb[-1]
    # split by 8-bits
    #print("error")
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    #print(all_bytes)
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        #decoded_data += str(np.base_repr(int(byte), base=16))
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]

def show_image(img_name):
    image = cv2.imread(img_name,-1)
    cv2.imshow("im",image)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    cv2.imshow("imag",image_rgb)
    binary_data = ""
    for row in image_rgb:
        for pixel in row:
            Y, Cr, Cb = to_bin(pixel)
            #binary_data += Y[-1]
            #binary_data += Cr[-1]
            binary_data += Cb[-1]
    print(binary_data)

# if __name__ == "__main__":
#     input_image = "VISION\supernova.jpg"
#     output_image = "encoded_image.PNG"
#     secret_data = "This is a top secret message."
#     im = cv2.imread("encoded_image.PNG",-1)
#     cv2.imshow("a",im)
#     # encode the data into the image
#     encoded_image = encode(image_name=input_image, secret_data=secret_data)
#     # save the output image (encoded image)
#     cv2.imwrite(output_image, encoded_image)
    
#     # # decode the secret data from the image
#     decoded_data = decode(output_image)
#     print("[+] Decoded data:", decoded_data)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

