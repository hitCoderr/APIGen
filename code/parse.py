from allennlp.predictors.predictor import Predictor

class TreeNode:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children is not None else []

def parse_tree(tree_str):
    # Parses a tree string into a TreeNode structure.
    tree_str = tree_str.strip()
    if not tree_str.startswith("("):
        return TreeNode(tree_str)
    label_end = tree_str.find(" ")
    label = tree_str[1:label_end]
    children = []
    remainder = tree_str[label_end+1:-1].strip()
    while remainder:
        if remainder[0] == "(":
            open_parens = 0
            for i, char in enumerate(remainder):
                if char == "(":
                    open_parens += 1
                elif char == ")":
                    open_parens -= 1
                    if open_parens == 0:
                        children.append(parse_tree(remainder[:i+1]))
                        remainder = remainder[i+1:].strip()
                        break
        else:
            space_index = remainder.find(" ")
            if space_index == -1:
                children.append(TreeNode(remainder))
                remainder = ""
            else:
                children.append(TreeNode(remainder[:space_index]))
                remainder = remainder[space_index:].strip()
    return TreeNode(label, children)

def match_pattern(node, pattern):
    # Matches specific structural patterns in the given tree node.
    matched_elements = {}

    if pattern == "VB+NP+PP/S" and node.label == "VP":
        if len(node.children) >= 3 and node.children[0].label.startswith("VB") and node.children[1].label == "NP":
            if node.children[2].label == "PP" or node.children[2].label == "S":
                matched_elements["VB"] = node.children[0]
                matched_elements["NP"] = node.children[1]
                matched_elements["PP/S"] = node.children[2]
        
    elif pattern == "VB+NP+PP+PP/S" and node.label == "VP":
        if len(node.children) >= 4 and node.children[0].label.startswith("VB") and node.children[1].label == "NP" and node.children[2].label == "PP":
            if node.children[3].label == "PP" or node.children[3].label == "S":
                matched_elements["VB"] = node.children[0]
                matched_elements["NP"] = node.children[1]
                matched_elements["PP1"] = node.children[2]
                matched_elements["PP/S"] = node.children[3]
            
    elif pattern == "VB+S" and node.label == "VP":
        if len(node.children) == 2 and node.children[0].label.startswith("VB") and node.children[1].label == "S":
            matched_elements["VB"] = node.children[0]
            matched_elements["S"] = node.children[1]
    # If the pattern is matched, return the elements
    if matched_elements:
        return matched_elements
    # Otherwise, check the children
    for child in node.children:
        result = match_pattern(child, pattern)
        if result:
            return result
    return None

def simplified_tree_to_string(node):
    # Converts a TreeNode into a simplified string representation.
    if not node.children:
        return node.label
    return f"{' '.join(simplified_tree_to_string(child) for child in node.children)}"


sentence = "convert a String to an int"
predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/elmo-constituency-parser-2020.02.10.tar.gz")
parsed_tree = predictor.predict(sentence=sentence)
tree_str = parsed_tree['trees']
root = parse_tree(tree_str)
structures = ["VB+NP+PP+PP/S","VB+NP+PP/S", "VB+S"]
matches = {structure: match_pattern(root, structure) for structure in structures}
simplified_matches_string = {}
for structure, elements in matches.items():
    if elements:
        simplified_matches_string[structure] = {key: simplified_tree_to_string(value) for key, value in elements.items()}

print(simplified_matches_string)