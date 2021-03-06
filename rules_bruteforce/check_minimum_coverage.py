
from validation_indices import NamedIndices
from numpy import sign

# set of rules to check
'''rules = (
    ((1, 1, 2, 3, 3, 2, 2, 2), (1, 1, 3, 2, 3, 2, 0, 2), (3, 1, 2, 3, 2, 2, 2, 1), "#rule 1#"),
    ((1, 1, 2, 3, 3, 2, 2, 2), (1, 1, 0, 0, 3, 2, 3, 2), (2, 2, 3, 0, 0, 3, 0, 2), "#rule 2#"),
    ((1, 1, 2, 3, 3, 2, 2, 2), (3, 0, 1, 2, 1, 0, 3, 2), (1, 3, 1, 1, 3, 3, 2, 3), "#rule 3#"),
    ((2, 1, 0, 0, 1, 0, 0, 2, 1), (2, 0, 1, 2, 0, 2, 2, 1, 0), (2, 0, 0, 0, 0, 1, 0, 2, 0), "#rule 4#"),
)'''
'''rules = (
    ((1, 0, 0, 0, 0, 0), (0, 2, 2, 0, 2, 2), (1, 2, 0, 0, 2, 2),"#rule 1#"),
    ((0, 1, 1, 4, 1, 2, 1, 3, 2, 3),(1, 3, 0, 0, 4, 2, 0, 0, 3, 4), (2, 4, 0, 4, 4, 4, 0, 0, 0, 0),"#rule 2#"),
    ((0, 0, 1, 2, 2, 2, 1, 2, 0, 0, 2, 1),(0, 1, 1, 2, 2, 2, 1, 0, 2, 0, 2, 0), (0, 0, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0),"#rule 3#"),
    ((3, 2, 0, 3, 0, 1, 2, 3, 1, 3, 0, 2, 3, 2, 3, 0),(2, 3, 2, 2, 3, 2, 0, 1, 3, 0, 3, 3, 1, 3, 1, 0), (2, 3, 0, 2, 1, 1, 1, 2, 1, 0, 1, 1, 2, 1, 1, 2),"#rule 4#")
)'''
# Works for avg-AMI and geo-AMI
rules = (
  ((1, 0, 0, 0, 0, 0), (0, 2, 2, 0, 2, 2), (1, 2, 0, 0, 2, 2), "#rule 1#"),
  ((0, 1, 1, 4, 1, 2, 1, 3, 2, 3), (1, 3, 0, 0, 4, 2, 0, 0, 3, 4), (2, 4, 0, 4, 4, 4, 0, 0, 0, 0), "#rule 2#"),
  ((0, 0, 1, 2, 2, 2, 1, 2, 0, 0, 2, 1), (0, 1, 1, 2, 2, 2, 1, 0, 2, 0, 2, 0), (0, 0, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0), "#rule 3#"),
  ((3, 2, 0, 3, 0, 1, 2, 3, 1, 3, 0, 2, 3, 2, 3, 0), (2, 3, 2, 2, 3, 2, 0, 1, 3, 0, 3, 3, 1, 3, 1, 0), (2, 3, 0, 2, 1, 1, 1, 2, 1, 0, 1, 1, 2, 1, 1, 2), "#rule 4#")
)

index2signs = dict()
signs2index = dict()
for name,I in NamedIndices.items():
    isdist = -1 if I.isdistance else 1
    signs = tuple(
        #str(int(sign(isdist*I.score(gt,p1)-isdist*I.score(gt,p2))))
        "L" if isdist*I.score(gt,p1)>=isdist*I.score(gt,p2) else "R"
        for gt,p1,p2,_ in rules
    )
    index2signs[name] = signs
    if signs in signs2index:
        print(name,"indistinguishable from",signs2index[signs])
    signs2index[signs] = name

# Print the indices and their signs
print("\t\t"+"\t".join(r[3] for r in rules))
for I_name,signs in index2signs.items():
    print(I_name+" "*(8-len(I_name))+"\t"+"\t\t".join(signs))

preferences = {
    "Rule "+str(i+1): {
        "L": [
            name
            for name,signs in index2signs.items()
            if signs[i]=="L"
        ],
        "R": [
            name
            for name,signs in index2signs.items()
            if signs[i]=="R"
        ],
    }
    for i in range(4)
}
for rule,preference in preferences.items():
    print(rule)
    print(", ".join(preference["L"]))
    print(", ".join(preference["R"]))