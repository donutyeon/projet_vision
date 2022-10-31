import cv2
import numpy as np

def to_bin(data,forma):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), forma) for i in data ])
    elif isinstance(data, bytes):
        return ''.join([ format(i, forma) for i in data ])
    elif isinstance(data, np.ndarray):
        return [ format(i, forma) for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint16):
        return format(data,forma)
    else:
        raise TypeError("Type not supported.")

def encode(img,message):
    image = cv2.imread(img)
    # maximum bytes to encode
    image_16 = np.uint16(image)
    image_16 *= 255
    image_y=cv2.cvtColor(image_16,cv2.COLOR_BGR2RGB)
    n_bytes_test = image_y.shape[0] * image_y.shape[1] * 3 // 16
    print((n_bytes_test))
    print("[*] Maximum bytes to encode:", n_bytes_test)
    if len(message) > n_bytes_test:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    # add stopping criteria
    message += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(message,"08b")
    print(binary_secret_data)
    data_len = len(message)
    for y in range(image_y.shape[0]):
        for x in range (image_y.shape[1]):
            Y,Cr,Cb=to_bin(image_y[y,x],'016b')
            if data_index < data_len:
                #print('before ',(image_y[y,x]))
                image_y[y,x,2] = ord(message[data_index])
                #print('after ',image_y[y,x,2])
                #print('after ',to_bin(image_y[y,x],'016b'))
                data_index += 1
            else:
                break
    print(image_y[0,0,2])
    print(image_y[0,1,2])
    image_s=cv2.cvtColor(image_y,cv2.COLOR_YCrCb2RGB)
    return image_s

def decode(image_name):
    print("[+] Decoding...")
    # read the image
    print(image_name)
    image = cv2.imread(image_name,-1)
    #cv2.imshow("im",image)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
    #cv2.imshow("im",image_rgb)
    #image_y = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
    binary_data = ""
    print(image_rgb[0,0]-4)
    print(image_rgb[0,1]-4)
    for y in range(image_rgb.shape[0]):
        for x in range (image_rgb.shape[1]):
            image_rgb[y,x,2]-=4
            Y,Cr,Cb=image_rgb[y,x]
            #binary_data += Y[-1]
            #binary_data += Cr[-1]
            binary_data += chr(Cb)
    
    # split by 8-bits
    #print("error")
    #all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    #print(all_bytes)
    #print(all_bytes)
    # convert from bits to characters
    decoded_data = ""
    for byte in binary_data:
        #decoded_data += str(np.base_repr(int(byte), base=16))
        decoded_data += byte
        if decoded_data[-1:] == "=====":
            break
    return decoded_data[:-1]