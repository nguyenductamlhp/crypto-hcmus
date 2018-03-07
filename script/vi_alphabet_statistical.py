# -*- coding: utf-8 -*-
from slugify import slugify
import string
import os
import re

def count_alphabet():
    """
    Return dict which contains rating of alplabet
    """
    list_file = []
    for file in os.listdir("."):
        if file.endswith(".txt"):
            list_file.append(os.path.join(".", file))
    result = {}
    for i in string.ascii_lowercase:
        result[i] = 0
    for file in list_file:
        f = open(file, 'r')
        content = f.read()
        content = slugify(content)
        content = content.replace("-", '')
        for char in content:
            if char in result.keys():
                result[char] = result[char] + 1
        f.close()
    return result
    
print count_alphabet()