from PIL import Image, ImageDraw
from itertools import product

# 0: empty base, 1: runner
all_base_combos = list(product([False, True], repeat=3))
print(all_base_combos)
all_outs = [0, 1, 2]

def draw_im(bases=[False, False, False], outs=0):
    base = Image.new("RGBA", (60, 60))

    outlined_square = Image.new("RGBA", (20, 20), (0, 0, 0, 0)) # background
    draw = ImageDraw.Draw(outlined_square)
    draw.rectangle([0, 0, 19, 19], fill=None, outline="white", width=2)

    empty_base = outlined_square.rotate(45, expand=True) # expand makes sure it expands past 20x20 to fit rotation

    filled_square = Image.new("RGBA", (20, 20), (0, 0, 0, 0)) # background
    draw = ImageDraw.Draw(filled_square)
    draw.rectangle([0, 0, 19, 19], fill="white")

    occupied_base = filled_square.rotate(45, expand=True) # expand makes sure it expands past 20x20 to fit rotation

    # 3rd
    base.paste(occupied_base if bases[2] else empty_base, (-1, 15), occupied_base if bases[2] else empty_base)

    # 2nd
    base.paste(occupied_base if bases[1] else empty_base, (15, -1), occupied_base if bases[1] else empty_base)

    # 1st
    base.paste(occupied_base if bases[0] else empty_base, (31, 15), occupied_base if bases[0] else empty_base)


    empty_circle = Image.new("RGBA", (15, 15), (0, 0, 0, 0)) # background
    draw = ImageDraw.Draw(empty_circle)
    draw.circle((7, 7), 7, fill=None, outline="white", width=2)

    filled_circle = Image.new("RGBA", (15, 15), (0, 0, 0, 0)) # background
    draw = ImageDraw.Draw(filled_circle)
    draw.circle((7, 7), 7, fill="white")

    # out 1
    base.paste(empty_circle if outs < 1 else filled_circle, (13, 45))#, circle)

    # out 2
    base.paste(empty_circle if outs < 2 else filled_circle, (32, 45))#, circle)

    file_name = f"bases/bases{int(bases[0])}{int(bases[1])}{int(bases[2])}_outs{outs}.png"

    base.save(file_name)

for base_combo in all_base_combos:
    for out_num in all_outs:
        draw_im(base_combo, out_num)