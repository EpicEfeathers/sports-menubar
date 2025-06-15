from PIL import Image, ImageDraw

def draw_im(bases=(False, False, False), outs=(False, False)):
    base = Image.new("RGBA", (60, 60)) # transparent background

    square = Image.new("RGBA", (20, 20), (0, 0, 0, 0)) # background
    draw = ImageDraw.Draw(square)
    draw.rectangle([0, 0, 19, 19], fill=None, outline="white", width=2) # solid red square

    # Step 3: Rotate the square by 45 degrees (expand makes sure it expands past 20x20 to fit rotation)
    rotated_square = square.rotate(45, expand=True)

    # 3rd
    base.paste(rotated_square, (-1, 15), rotated_square)

    # 2nd
    base.paste(rotated_square, (15, -1), rotated_square)

    #1st
    base.paste(rotated_square, (31, 15), rotated_square)


    circle = Image.new("RGBA", (15, 15), (0, 0, 0, 0)) # background
    draw = ImageDraw.Draw(circle)
    draw.circle((7, 7), 7, fill=None, outline="white", width=2)

    # out 1
    base.paste(circle, (13, 45), circle)

    # out 2
    base.paste(circle, (32, 45), circle)

    base.save("bases/info.png")