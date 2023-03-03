from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def break_fix(text, width, font, draw):
    if not text:
        return
    lo = 0
    hi = len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        t = text[:mid]
        w, h = draw.textsize(t, font=font)
        if w <= width:
            lo = mid
        else:
            hi = mid - 1
    t = text[:lo]
    w, h = draw.textsize(t, font=font)
    yield t, w, h
    yield from break_fix(text[lo:], width, font, draw)


def fit_text(img, text, color, font):
    width = img.size[0] - 2
    draw = ImageDraw.Draw(img)
    pieces = list(break_fix(text, width, font, draw))
    height = sum(p[2] for p in pieces)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")
    y = (img.size[1] - height) // 1.03
    for t, w, h in pieces:
        x = (img.size[0] - w) // 2
        draw.text((x, y), t, font=font, stroke_width=2, stroke_fill='black')
        y += h


def shelby_meme(text, sample=3):
    if len(text) == 0:
        print("No text")
        return 1
    # if len(text) > 25:
    #     print("Too long text")
    #     return 1
    img = Image.open(f'samples/{sample}resize.jpg')
    w, h = img.size

    my_image = ImageDraw.Draw(img)
    font = ImageFont.truetype("impact.ttf", 48)
    #text_w, text_h = my_image.textsize(text, font)

    #my_image.text(((w - text_w) // 2, h - text_h - 15), text, (255,255,255), font=font, stroke_width=2, stroke_fill='black')
    fit_text(img, text, (255, 255, 255), font)
    img.save("meme.jpg")

shelby_meme('ебаная чурчхелла', 3)
