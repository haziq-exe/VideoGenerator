from ButtonFetch import ButtonFetch

def RefineScript(Positive, Negative):

    Script = "Will you push the button?\nIf you do then"

    for i in range(len(Positive)):
        Script += f"::_: {Positive[i]} but:_:: {Negative[i]}. So are you pushing the button?_:_:_\n\n\n\n\n\n\n\n\n\n\n\n"

    Script = Script[:(len(Script) - 6)]
    Script += "\nHit the follow button for a variety of different content daily"

    return Script