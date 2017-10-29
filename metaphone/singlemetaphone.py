# -*- coding: utf-8 -*-

def singlemetaphone(text, method = 1):  # method 1 == single, method 2 == double
    
    length = len(text)
    text = text.lower()
    vokaler = ['a','e','i','o','u','æ','ø','å']
    res = ""
    rule_used = False
    j = 1
    if method == 1:
        for i in text:
# length 1 substitution rules
            if i  == "w" and rule_used == False:
                res += "v"
                rule_used = True

            elif i == "c" and rule_used == False:
                res += "k"
                rule_used = True

            elif i == "ü" and rule_used == False:
                res += "y"
                rule_used = True

            elif i == "x" and rule_used == False:
                res += "ks"
                rule_used = True

# Skipping Rules
            elif i == "h" and rule_used == False:
                if j >= 2:
                    if (text[j-2] == "c"):
                        res += ""
                        rule_used = True
                    elif(text[j-2] == "t"):
                        res += ""
                        rule_used = True
                    elif (text[j - 2] != "p" and rule_used == False):
                        res += i
                        rule_used = True

            elif i == "s" and rule_used == False:
                if j >= 2:
                    if text[j - 2] != "d":
                        res += i
                    rule_used = True

# length 2 -> 1 substitution rules
# vowel based rules doesn't have antirules, cause, they will be removed anyway.
            elif j < length and rule_used == False:
                if text[j-1] == "p":
                    if text[j] == "h":
                        res += "f"
                        rule_used = True

                elif text[j-1] == "d":
                    if text[j] == "s":
                        res += "s"
                        rule_used = True

                elif text[j - 1] == "i" and length > j+1 and text[j-2] != "e":  # remember that this rule type requires that the method is run on a string with no spaces so not "marie hadoukin" this will giver "mrj something" where "marie" will give "mr" which is what we want
                    if text[j] == "e":
                        res += "j"
                        rule_used = True

                elif i == "e"  and text[j-2] != "i":
                    if text[j] == "i":
                        res += "j"
                        rule_used = True


                elif i == "ø":
                    if text[j] == "i":
                        res += "j"
                        rule_used = True

            if rule_used == False:
                res += i
            else:
                rule_used = False
            j += 1

        res = res.translate(None, "".join(vokaler)) # Fjerner alle vokaler
        # print "res: " + res
        return res


    if method == 2:
        for i in text:
            if i == "w" and rule_used == False:
                res += "v"
                rule_used = True

            elif i == "c" and rule_used == False:
                res += "k"
                rule_used = True


            elif i == "ü" and rule_used == False:
                i = "y"
                res += "y"
                rule_used = True

            elif i == "h" and rule_used == False:
                if j > 2:
                    if (text[j - 2] != "p"):
                        res += i
                    rule_used = True

            elif i == "s" and rule_used == False:
                if j > 2:
                    if (text[j - 2] != "d"):
                        res += i
                    rule_used = True

            elif i == "u" and rule_used == False:
                if j > 2:
                    if (text[j - 2] == "q"):
                        res += "v"
                    rule_used = True
                else:
                    res += i
                    rule_used = True


            elif j < length and rule_used == False:
                if text[j - 1] == "p":
                    if text[j] == "h":
                        res += "f"
                        rule_used = True

                if text[j - 1] == "d":
                    if text[j] == "s":
                        res += "s"
                        rule_used = True

                if text[j - 1] == "q":
                    if text[j] == "u":
                        res += "k"
                        rule_used = True

            if rule_used == False:
                res += i
            else:
                rule_used = False
            j += 1

    res = res.translate(None, "".join(vokaler)) # Fjerner alle vokaler
    # print "res: " + res


    return res
