import spacy

def analyze_syntax(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    roles = {
        "verb": None,
        "direct object": None,
        "direct object's modifier": None,
        "preposition": None,
        "preposition object": None,
        "preposition object's modifier": None
    }

    for token in doc:
        if token.dep_ == "ROOT":
            roles["verb"] = token.text
        elif token.dep_ == "dobj":
            roles["direct object"] = token.text
            if token.children:
                for child in token.children:
                    if child.dep_ == "det":
                        roles["direct object's modifier"] = child.text
        elif token.dep_ == "prep":
            roles["preposition"] = token.text
            for child in token.children:
                if child.dep_ == "pobj":
                    roles["preposition object"] = child.text
                    if child.children:
                        for grandchild in child.children:
                            if grandchild.dep_ == "det":
                                roles["preposition object's modifier"] = grandchild.text

    return roles

# Test the function
sentence = "convert a String to an int"
analyzed_roles = analyze_syntax(sentence)
print(analyzed_roles)
