# image handling API

images = {}

def add_image(data, user):
#    if images:
#        image_num = max(images.keys()) + 1
#    else:
#        image_num = 0
        
#    images[image_num] = data
#    return image_num

#def get_image(num):
#    return images[num]
    images[user] = data
    return user

def get_image(user):
    return images[user]


def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]
