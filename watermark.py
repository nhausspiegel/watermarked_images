from PIL import Image, ImageDraw, ImageFont
from numpy import random
import os, os.path
from tqdm import tqdm


def random_position(im_width, im_height, text_width, text_height):
    return (random.randint(im_width - text_width), random.randint(im_height - text_height))

#TODO (possibly): use this function
def random_color():
    pass


# def random_word(words):
#     return random.choice(words)
    
    
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst
    
    
def apply_watermark(image_path, watermark_text):
    
    random_angle = random.rand()*360
    
    # chosen bc of pix2pix.
    dim = 256
    
    with Image.open(image_path).convert("RGBA") as base:
        
        # initial setup
        
        im_width, im_height = base.size
        
        if im_width < 256:
            base = base.resize((256, int(im_height * (256 / im_width))))
        if im_height < 256:
            base = base.resize((int(im_width * (256 / im_height)), 256))
        
        im_width, im_height = base.size
                
        if im_width - dim == 0:
            x1 = 0
        else:
            x1 = random.randint(im_width - dim)
        if im_height - dim == 0:
            y1 = 0
        else:
            y1 = random.randint(im_height - dim)

        base = base.crop((x1, y1, x1 + dim, y1 + dim))

        # from here on out we are dealing with 256x256 images.
        
        img = base
                
        # get a font at a random size
        # 50 is max value for now.
        fnt = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Black.ttf", random.randint(10, high=50))
        
        txt_test = Image.new("RGBA", (dim, dim), (255, 255, 255, 0))
        d_test = ImageDraw.Draw(txt_test)
        d_test.text((dim // 2, dim // 2), watermark_text, font=fnt, fill=(255, 255, 255, 255))
        w_test = txt_test.rotate(random_angle)
        
        try:
            x0, y0, x1, y1 = w_test.getbbox()
        except:
            x0, y0, x1, y1 = 0, 0, 0, 0
        
        position = random_position(dim, dim, x1 - x0, y1 - y0)
        
        # make a blank image for the text, initialized to transparent text color
        txt = Image.new("RGBA", (dim, dim), (255, 255, 255, 0))
        # get a drawing context
        d = ImageDraw.Draw(txt)
        # draw text
        d.text(position, watermark_text, font=fnt, fill=(255, 255, 255, 128))
        
        w = txt.rotate(random_angle)
                
        out = Image.alpha_composite(img, w)
        
        final = get_concat_h(base, out)
        
        return final
        


if __name__ == "__main__":
    
    image_paths = ['images/no-watermark/' + path for path in os.listdir('images/no-watermark')]
    
    # shuffle the images !!
    random.shuffle([image_paths])
    
    # count images
    # this works. trust
    N = len([name for name in image_paths])
    print(N)
    
    with open('words.txt', "r") as word_list:
        words = [word.rstrip() for word in word_list][:N]
        
        # applying watermarks to 15,000 images.
        # this is (almost) all the images we have:
        # 10,000 train, 2,500 val, 2,500 test.
        for i, path in enumerate(tqdm(image_paths[:15000])):
            img = apply_watermark(path, words[i])
            if i < 10000:
                img.save(f"images/watermark/train/{i}.jpg")
            elif i < 12500:
                img.save(f"images/watermark/val/{i}.jpg")
            else:
                img.save(f"images/watermark/test/{i}.jpg")
                