
from simpleimage import SimpleImage

def main():
    filename = get_file()
    image = SimpleImage(filename)
    image.show()
    filter = input("Enter the filter you want :\n Adjust Brightness\nChannel\nGreen-Screening\nTwin\nRelflect\nBorder\nGet RGB\nCyclone Highlight:\n")
    if filter == "Adjust Brightness":
        bright = adjust_brightness(image)
        bright.show()
    elif filter == "Channel":
        color = input("Which channel do you want? Red, Green or Blue? ")
        channel_image = channel(image,color)
        channel_image.show()
    elif filter == "Green-Screening":
        print("Enter the background file: ")
        back_file = get_file()
        image_back = SimpleImage(back_file)
        image_back.show()
        green_screened = green_screening(image,image_back)
        green_screened.show()
    elif filter == "Twin":
        twin_image = twin(image)
        twin_image.show()
    elif filter == "Reflect":
        reflected_image = reflect(image)
        reflected_image.show()
    elif filter == "Border":
        border_size = int(input("Enter the border size: "))
        bordered_image = border(image,border_size)
        bordered_image.show()
    elif filter == "Get RGB":
        x = int(input("Enter the x coordinate: "))
        y = int(input("Enter the y coordinate: "))
        values = get_rgb(image,x,y)
        print(values)
    elif filter == "Cyclone Highlight":
        cyclone_image = cyclone(image)
        cyclone_image.show()
    else:
        print("Invalid choice")

def adjust_brightness(image):
    new_image = image
    brightness_type = input("Choose between 1. Darken or 2. Brighten: ")
    factor = float(input("Enter the factor by which you want to change the image: "))
    # To Darken the image we divide the RGB values of each pixel by the factor
    if brightness_type == "Darken":
        for pixel in new_image:
            pixel.red //= factor
            pixel.green //= factor
            pixel.blue //= factor
        return new_image
    # To Brighten the image we multiply the RGB values of each pixel by the factor
    elif brightness_type == "Brighten":
        for pixel in new_image:
            pixel.red *= factor
            pixel.green *= factor
            pixel.blue *= factor
        return new_image

def channel(image,color):
    #Remove the other two channels to get the single channel
    for pixel in image:
        if color == "Red":
            pixel.green = 0
            pixel.blue = 0
        elif color == "Green":
            pixel.red = 0
            pixel.blue = 0
        else:
            pixel.red = 0
            pixel.green = 0
    return image
def green_screening(main_filename,back_filename):
    #Replacing the sufficiently green pixels with the background image
    intensity_threshold = 1.1
    image = main_filename
    back = back_filename
    for pixel in image:
        average = (pixel.red + pixel.green + pixel.blue) // 3
        # See if this pixel is "sufficiently" green
        if pixel.green >= average * intensity_threshold:
            # If so, we get the corresponding pixel from the
            # back image and overwrite the pixel in
            # the main image with that from the back image.
            x = pixel.x
            y = pixel.y
            image.set_pixel(x, y, back.get_pixel(x, y))
    return image

def twin(image):
    #Create a blank canvas with twice the width
    new_image = image
    width = new_image.width
    height = new_image.height
    mirror = SimpleImage.blank(width * 2, height)
    #Placing the  pixels in the right order
    for x in range(width):
        for y in range(height):
            pixel = new_image.get_pixel(x, y)
            mirror.set_pixel(x, y, pixel)
            mirror.set_pixel((width*2)-(x+1), y, pixel)
    return mirror

def reflect(image):
    new_image = image
    width = new_image.width
    height = new_image.height
    mirror = SimpleImage.blank(width , height*2)
    # Placing the  pixels in the right order
    for x in range(width):
        for y in range(height):
            pixel = new_image.get_pixel(x, y)
            mirror.set_pixel(x, y, pixel)
            mirror.set_pixel(x,(height * 2) - (y + 1), pixel)
    return mirror

def border(image,border_size):
    new_image = image
    new_width = new_image.width + 2 * border_size
    new_height = new_image.height + 2 * border_size

    # gives us a blank image of size new_width and new_height
    bordered_img = SimpleImage.blank(new_width, new_height)

    for x in range(bordered_img.width):
        for y in range(bordered_img.height):
            if is_border_pixel(x, y, border_size, bordered_img):
                pixel = bordered_img.get_pixel(x, y)
                pixel.red = 0
                pixel.green = 0
                pixel.blue = 0
            else:
                # need to set pixel originally at (x,y) to shifted new position
                orig_x = x - border_size
                orig_y = y - border_size
                orig_pixel = new_image.get_pixel(orig_x, orig_y)
                bordered_img.set_pixel(x, y, orig_pixel)

    return bordered_img
def is_border_pixel(x, y, border_size, bordered_img):
    """
    This function returns true or false based on whether the pixel at (x, y)
    is part of the border or not.

    Inputs:
        - x: The x position of the pixel
        - y: The y position of the pixel
        - border_size: The thickness of the border
        - bordered_img: The bordered image

    Returns:
        True or false based on whether the pixel at (x,y) is a border pixel
        i.e. should be coloured black.
    """
    # left border
    if x < border_size:
        return True
    # right border
    if x >= bordered_img.width - border_size:
        return True
    # top border
    if y < border_size:
        return True
    # bottom border
    if y >= bordered_img.height - border_size:
        return True

    return False

def get_rgb(image,x,y):
    new_image = image
    pixel = new_image.get_pixel(x, y)
    return pixel.red, pixel.green, pixel.blue


def cyclone(image):
    for pixel in image:
        if pixel.red>190 and pixel.green>190 and pixel.blue>190:
            pixel.green = 0
            pixel.blue = 0
        else:
            pixel.red //=2
            pixel.green //=2
            pixel.blue //=2
    return image


def get_file():
    # Read image file path from user, or use the default file
    filename = input('Enter image file : ')
    return filename

if __name__ == '__main__':
    main()