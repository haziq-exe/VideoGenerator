import sys
import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(parent_directory, 'RedditTypeVideo'))
import ImageGen
from CommentFetch import load_comments

num_comments = 50
Run_Number = 13


fullycompleted = False
Question, Comments = load_comments(numofcomments=num_comments)
Question = Question[0]
ImageGen.create_SlideShowpost(Question=Question, gennumber=Run_Number)
success = 0

for i in range(len(Comments)):
    successful = ImageGen.create_comment(Comments[i], gennumber=Run_Number, slidenumber=(i+1))
    if successful:
        success += 1
    if success == num_comments:
        break