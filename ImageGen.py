from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import re

#Width: 118 (from left) 145 (from right)
#Height: 317 from bottom 177 from top
#Max pixels: 1005


def create_post(title, file_name, week_number): #Add title

    image_path = '/Users/haziq/Desktop/TikTokGenerator/PostImage/PostTemplate.png'
    image = Image.open(image_path)

    draw = ImageDraw.Draw(image)

    font_path = '/Users/haziq/Library/Fonts/TikTok Sans Bold.ttf'
    font_size = 45
    font = ImageFont.truetype(font_path, font_size)


    max_width = 1005 - 110
    lines = []
    editedtitle = title.replace(":_:", " ")
    words = editedtitle.split()
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        boxsize = draw.textbbox((0,0), test_line, font=font)
        line_width = boxsize[2] - boxsize[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line not in lines:
        lines.append(current_line)



    xposition = 110
    yposition = 215 - (8 * len(lines))

    if len(lines) > 4:
        font_size = font_size - ((len(lines) - 4) * 8)
    if len(lines) == 2:
        font_size = 75
        yposition = 230
    if len(lines) == 1:
        font_size = 90
        yposition = 260
    if len(lines) == 8:
        font_size = 10
    if len(lines) > 8:
        return print("ERROR: too many lines in title bruv")

    for line in lines:
        draw.text((xposition,yposition), line, fill='white', font=font)
        if len(lines) == 8:
            yposition += (font_size + 26)
        else:
            yposition += (font_size + 17)

    image.save(f'/Users/haziq/Desktop/TikTokGenerator/PostImage/FinalPostImages/week{week_number}/{file_name}.png')


def create_comment(comment_text, gennumber, slidenumber, HugePost = False):

    font_path = '/System/Library/Fonts/Supplemental/Verdana.ttf'
    font_size = 25
    font = ImageFont.truetype(font_path, font_size)
    padding = 20
    corner_radius = 20
    max_width = 1005 - 110
    xposition = padding + 35
    yposition = padding + 65


    if HugePost == True:
        max_width = 1005 - 310
        font_size = 20
        yposition = padding + 60


    words = comment_text.split(' ')
    # for i, word in enumerate(words):
    #     print(word)
    #     if '\n' in word:
    #         word.replace('\n', " lineend ")
    #         # words.insert(i + 1, 'lineend')
    

    image_width = max_width + 100

    imagetemp = Image.new("RGBA", (image_width, (font_size + padding)), (255, 255, 255, 0))
    draw = ImageDraw.Draw(imagetemp)


    lines = []
    current_line = ""
    image_height = 100
    line_gap = 15


    for word in words:
        test_line = f"{current_line} {word}".strip()
        boxsize = draw.textbbox((0,0), test_line, font=font)
        line_width = boxsize[2] - boxsize[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            if 'http' in word:
                pattern = r"http[s]?://\S+"
                word = re.sub(pattern, "[Link]", word)
            lines.append(current_line)
            current_line = word

    if current_line not in lines:
        lines.append(current_line)

    for line in lines:
        boxsize = draw.textbbox((0,0), line, font=font)
        line_height = boxsize[3] - boxsize[1]
        image_height += line_height + line_gap

    # image_height += (16 * len(lines)) + ((font_size + 3) * extraends) + ((font_size + 3) * len(lines))

    image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        [(0, 0), (image_width, image_height)],
        # radius=corner_radius,
        fill='black'
    )

    xposition = padding + 35
    yposition = padding + 65

    load_pfp_image = Image.open("/Users/haziq/Desktop/TikTokGenerator/PostImage/CommentElements/PFP.png")
    pfp_image = load_pfp_image.resize((60,60))
    pfp_position = (5,10)
    image.paste(pfp_image, pfp_position, pfp_image)

    load_share = Image.open('/Users/haziq/Desktop/TikTokGenerator/PostImage/CommentElements/Share.png')
    share_img = load_share.resize((17,17))
    share_pos = ((image_width - 30), (image_height - 22))
    image.paste(share_img, share_pos, share_img)

    load_upvote = Image.open('/Users/haziq/Desktop/TikTokGenerator/PostImage/CommentElements/Upvote.png')
    upvote_img = load_upvote.resize((30,30))
    upvote_pos = ((padding), (image_height - 30))
    image.paste(upvote_img, upvote_pos, upvote_img)

    draw.text((65, 35), "u_redditstories   • Just now", fill='gray', font=font)

    for line in lines:
        draw.text((xposition,yposition), line, fill='white', font=font)
        boxsize = draw.textbbox((0,0), line, font=font)
        line_height = boxsize[3] - boxsize[1]
        yposition += (line_height + line_gap)

    linestart = (35,70)
    lineend = (35, yposition - 16)
    draw.line([linestart, lineend], fill=(90,90,90), width=1)



    image.save(f"/Users/haziq/Desktop/TikTokGenerator/Slideshows/GenNumber{gennumber}/slide{slidenumber}.png")

    print(f'SLIDE {slidenumber}: HEIGHT={image_height}')

    if image_height > 1500 and HugePost == False:
        create_comment(comment_text=comment_text, gennumber=gennumber, slidenumber=slidenumber, HugePost=True)
        print(f'Huge Post for Slide {slidenumber}')

def create_SlideShowpost(Question, gennumber):

    os.makedirs(f'/Users/haziq/Desktop/TikTokGenerator/SlideShows/GenNumber{gennumber}', exist_ok=True)

    image_path = '/Users/haziq/Desktop/TikTokGenerator/PostImage/PostTemplate.png'
    image = Image.open(image_path)

    draw = ImageDraw.Draw(image)

    font_path = '/Users/haziq/Library/Fonts/TikTok Sans Bold.ttf'
    font_size = 45
    font = ImageFont.truetype(font_path, font_size)


    max_width = 1005 - 110
    lines = []
    words = Question.split()
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        boxsize = draw.textbbox((0,0), test_line, font=font)
        line_width = boxsize[2] - boxsize[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line not in lines:
        lines.append(current_line)



    xposition = 110
    yposition = 215 - (8 * len(lines))

    if len(lines) > 4:
        font_size = font_size - ((len(lines) - 4) * 8)
    if len(lines) == 2:
        font_size = 75
        yposition = 230
    if len(lines) == 1:
        font_size = 90
        yposition = 260
    if len(lines) == 8:
        font_size = 10
    if len(lines) > 8:
        return print("ERROR: too many lines in title bruv")

    for line in lines:
        draw.text((xposition,yposition), line, fill='white', font=font)
        if len(lines) == 8:
            yposition += (font_size + 26)
        else:
            yposition += (font_size + 17)

    image.save(f'/Users/haziq/Desktop/TikTokGenerator/Slideshows/GenNumber{gennumber}/Question.png')