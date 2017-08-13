# -*- coding: utf-8 -*-


def singlemetaphone(text, method) : #method 1 == single, method 2 == double

    length = len(text)
    text = text.lower()
    vokaler = ['a','e','i','o','u','æ','ø','å']
    res = ""
    ruleUsed = False
    j = 1
    if method == 1 :
        for i in text :
# length 1 substitution rules
            if i  == "w" and ruleUsed == False :
                res += "v"
                ruleUsed = True

            elif i == "c" and ruleUsed == False :
                res += "k"
                ruleUsed = True


            elif i == "ü" and ruleUsed == False :
                res += "y"
                ruleUsed = True

            elif i == "x" and ruleUsed == False:
                res += "ks"
                ruleUsed = True

# Skipping Rules
            elif i == "h" and ruleUsed == False:
                if j > 2 :
                    if (text[j - 2] != "p") :
                        res += i
                    ruleUsed = True

            elif i == "s" and ruleUsed == False:
                if j > 2 :
                    if text[j - 2] != "d" :
                        res += i
                    ruleUsed = True

# length 2 -> 1 substitution rules
# vowel based rules doesn't have antirules, cause, they will be removed anyway.
            elif j < length and ruleUsed == False:
                if text[j-1] == "p" :
                    if text[j] == "h" :
                        res += "f"
                        ruleUsed = True

                elif text[j-1] == "d" :
                    if text[j] == "s" :
                        res += "s"
                        ruleUsed = True

                elif text[j - 1] == "i" and length > j+1 and text[j-2] != "e": #remember that this rule type requires that the method is run on a string with no spaces so not "marie hadoukin" this will giver "mrj something" where "marie" will give "mr" which is what we want
                    if text[j] == "e":
                        res += "j"
                        ruleUsed = True

                elif i == "e"  and text[j-2] != "i" :
                    if text[j] == "i" :
                        res += "j"
                        ruleUsed = True


                elif i == "ø" :
                    if text[j] == "i" :
                        res += "j"
                        ruleUsed = True

            if ruleUsed == False :
                res += i
            else :
                ruleUsed = False
            j += 1

        res = res.translate(None, "".join(vokaler)) # Fjerner alle vokaler
        print "res: " + res
        return text


    if method == 2:
        for i in text:
            if i == "w" and ruleUsed == False:
                res += "v"
                ruleUsed = True

            elif i == "c" and ruleUsed == False:
                res += "k"
                ruleUsed = True


            elif i == "ü" and ruleUsed == False:
                i = "y"
                res += "y"
                ruleUsed = True

            elif i == "h" and ruleUsed == False:
                if j > 2:
                    if (text[j - 2] != "p"):
                        res += i
                    ruleUsed = True

            elif i == "s" and ruleUsed == False:
                if j > 2:
                    if (text[j - 2] != "d"):
                        res += i
                    ruleUsed = True

            elif i == "u" and ruleUsed == False:
                if j > 2:
                    if (text[j - 2] == "q"):
                        res += "v"
                    ruleUsed = True
                else :
                    res += i
                    ruleUsed = True


            elif j < length and ruleUsed == False:
                if text[j - 1] == "p":
                    if text[j] == "h":
                        res += "f"
                        ruleUsed = True

                if text[j - 1] == "d":
                    if text[j] == "s":
                        res += "s"
                        ruleUsed = True

                if text[j - 1] == "q":
                    if text[j] == "u":
                        res += "k"
                        ruleUsed = True

            if ruleUsed == False:
                res += i
            else:
                ruleUsed = False
            j += 1

    res = res.translate(None, "".join(vokaler)) # Fjerner alle vokaler
    print "res: " + res


    return text




