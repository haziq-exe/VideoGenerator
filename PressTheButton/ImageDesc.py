from PIL import Image, ImageDraw, ImageFont
import nltk
from nltk import word_tokenize, pos_tag
import re

def custom_tokenize(text):
    # Use regex to keep apostrophes and other punctuation attached to words
    tokens = re.findall(r"\w+(?:'\w+)?[\.,!?;]*|\w+", text)
    return tokens


def AddDesc(gennumber, numofquestions, positive, negative):

    font_path = '/Users/haziq/Library/Fonts/SummerFavourite-ARLr6.ttf'
    font_size = 100
    font = ImageFont.truetype(font_path, font_size)
    IMAGE_W = 1000
    IMAGE_H = 923

    for i in range(numofquestions):
        transparent_image_pos = Image.new("RGBA", (IMAGE_W, IMAGE_H), (0, 0, 0, 0))

        # Initialize drawing context
        draw_pos = ImageDraw.Draw(transparent_image_pos)

        lines = []
        current_line = ""
        pos_prompt = positive[i]
        pos_words = pos_prompt.split()

        for word in pos_words:
            test_line = f"{current_line} {word}".strip()
            boxsize = draw_pos.textbbox((0,0), test_line, font=font)
            line_width = boxsize[2] - boxsize[0]

            if line_width <= IMAGE_W - 20:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line not in lines:
            lines.append(current_line)
        

        for c, line in enumerate(lines):
            textbox = draw_pos.textbbox((0,0), line, font=font)
            text_width = textbox[2] - textbox[0]
            text_height = textbox[3] - textbox[1]
            y = ((IMAGE_H - text_height) // 2) - 280
            x = ((IMAGE_W - text_width) // 2) + 20
            y += (font_size + 10) * c

            bbox = draw_pos.textbbox((x,y), line, font=font)

            textbox_x0 = bbox[0] - 5
            textbox_y0 = bbox[1] - 5
            textbox_x1 = bbox[2] + 5
            textbox_y1 = bbox[3] + 5


            # textbox_x0 = (IMAGE_W - (textbox_x1 - textbox_x0)) // 2
            # textbox_x1 = textbox_x0 + (bbox[2] - bbox[0]) + 2 * 8
            # textbox_y0 = (IMAGE_H - (textbox_y1 - textbox_y0)) // 2
            # textbox_y1 = textbox_y0 + (bbox[3] - bbox[1]) + 2 * 8

            draw_pos.rectangle([textbox_x0, textbox_y0, textbox_x1, textbox_y1], fill="black")

            words = custom_tokenize(line)
            pos_tags = pos_tag(words)
            print(pos_tags)
            for word, pos in pos_tags:
                if pos in ["NN", "NNS", "NNP", "NNPS"]:
                    color = '#02B3F1'
                else:
                    color = 'white'
                
                # Draw the word
                draw_pos.text((x, y), word, font=font, fill=color)
    
                bbox = draw_pos.textbbox((0,0),word, font=font)
                word_width = bbox[2] - bbox[0]
                space_bbox = draw_pos.textbbox((0,0)," ", font=font)
                space_width = space_bbox[2] - space_bbox[0]
                x += word_width + space_width


            #draw_pos.text((x, y), line, font=font, fill="white")

        transparent_image_pos.save(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results/Q{i}-Desc.png')

        transparent_image_neg = Image.new("RGBA", (IMAGE_W, IMAGE_H), (0, 0, 0, 0))

        draw_neg = ImageDraw.Draw(transparent_image_neg)

        lines = []
        current_line = ""
        neg_prompt = negative[i]
        neg_words = neg_prompt.split()

        for word in neg_words:
            test_line = f"{current_line} {word}".strip()
            boxsize = draw_neg.textbbox((0,0), test_line, font=font)
            line_width = boxsize[2] - boxsize[0]

            if line_width <= IMAGE_W - 20:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line not in lines:
            lines.append(current_line)

        for c, line in enumerate(lines):
            textbox = draw_neg.textbbox((0,0), line, font=font)
            text_width = textbox[2] - textbox[0]
            text_height = textbox[3] - textbox[1]
            y = ((IMAGE_H - text_height) // 2) - 280
            x = ((IMAGE_W - text_width) // 2) + 20
            y += (font_size + 10) * c

            bbox = draw_neg.textbbox((x, y), line, font=font)

            textbox_x0 = bbox[0] - 5
            textbox_y0 = bbox[1] - 5
            textbox_x1 = bbox[2] + 5
            textbox_y1 = bbox[3] + 5


            draw_neg.rectangle([textbox_x0, textbox_y0, textbox_x1, textbox_y1], fill="black")

            words = custom_tokenize(line)
            pos_tags = pos_tag(words)
            print(pos_tags)
            for word, pos in pos_tags:
                if pos in ["NN", "NNS", "NNP", "NNPS"]:
                    color = '#F64D03'
                else:
                    color = 'white'
                
                # Draw the word
                draw_neg.text((x, y), word, font=font, fill=color)
    
                bbox = draw_neg.textbbox((0,0),word, font=font)
                word_width = bbox[2] - bbox[0]
                space_bbox = draw_neg.textbbox((0,0)," ", font=font)
                space_width = space_bbox[2] - space_bbox[0]
                x += word_width + space_width


        transparent_image_neg.save(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Conditions/Q{i}-Desc.png')

# def AddDesc(gennumber, numofquestions, positive, negative):

#     font_path = '/Users/haziq/Library/Fonts/TikTok Sans Bold.ttf'
#     font_size = 150
#     font = ImageFont.truetype(font_path, font_size)
#     IMAGE_W = 1024
#     IMAGE_H = 1024

#     for i in range(numofquestions):
#         image_path_pos = f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results/Q{i}.png'
#         image_pos = Image.open(image_path_pos)
#         draw_pos = ImageDraw.Draw(image_pos)

#         lines = []
#         current_line = ""
#         pos_prompt = positive[i]
#         pos_words = pos_prompt.split()

#         for word in pos_words:
#             test_line = f"{current_line} {word}".strip()
#             boxsize = draw_pos.textbbox((0,0), test_line, font=font)
#             line_width = boxsize[2] - boxsize[0]

#             if line_width <= IMAGE_W:
#                 current_line = test_line
#             else:
#                 lines.append(current_line)
#                 current_line = word
#             print(word)

#         if current_line not in lines:
#             lines.append(current_line)

        
#         # xposition = 50
#         yposition = 420 - (8 * len(lines))

#         for x, line in enumerate(lines):
#             print(len(line))
#             if x == 0:
#                 xposition = 260 - (15 * len(line))
#             draw_pos.text((xposition,yposition), line, fill='white', font=font)
#             yposition += (font_size + 17)

#         image_pos.save(f'/Users/haziq/Desktop/TikTokGenerator/PressTheButton/Images/GenNumber{gennumber}/Results/Q{i}-Test.png')
    
