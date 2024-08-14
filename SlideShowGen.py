from ImageGen import create_comment, create_SlideShowpost
from CommentFetch import load_comments

num_comments = 14

Question, Comments = load_comments(numofcomments=num_comments)

Question = Question[0]

Run_Number = 6

create_SlideShowpost(Question=Question, gennumber=Run_Number)

for i in range(len(Comments)):
    create_comment(Comments[i], gennumber=Run_Number, slidenumber=(i+1))
