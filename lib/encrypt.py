def reverse_string(s):
    result = ""
    for i in range(len(s)-1, -1, -1):
        result += s[i]
    return result


def count_vowels(s):
    count = 0
    for c in s:
        if c.lower() in ['a', 'e', 'i', 'o', 'u']:
            count += 1
    return count
