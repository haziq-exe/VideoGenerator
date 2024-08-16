from ButtonFetch import ButtonFetch, FetchImageDescriptions, FetchImages
from ScriptRefine import RefineScript
from SpeechGen import SpeechGen
from VideoGen import audio_replace, ImageAdd, FinalTouches

gen_number = 1

num_questions = 3
positive, negative = ButtonFetch(numofquestions=num_questions)
print(positive, negative)
positive_img, negative_img = FetchImageDescriptions(Result=positive, Condition=negative)
print(positive_img, negative_img)
FetchImages(gennumber=gen_number, ImgR=positive_img, ImgC=negative_img)

script = RefineScript(positive, negative)
posStart, negStart, wholeEnd = SpeechGen(script=script, gennumber=gen_number, speaker="Will", pitch=0.95)

audio_replace(gennumber=gen_number, pos_start=posStart, neg_start=negStart, whole_end=wholeEnd)
ImageAdd(pos_start=posStart, neg_start=negStart, whole_end=wholeEnd, gennumber=gen_number)
FinalTouches(pos_start=posStart, neg_start=negStart, whole_end=wholeEnd, gennumber=gen_number)