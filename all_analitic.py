import json
import os
import io


def group(group_name,word_group):
   
    
    with io.open(f"{group_name}/groups_{group_name}.txt", encoding='utf-8') as file:
        b = 0
        for line in file:
            if word_group in line:
                b += 1
    if b == 1:
        with open(f"{group_name}/Rezult_{group_name}.txt", "w", encoding='utf-8') as file_end:
            file_end.write("не подходит")
    else:
        with open(f"{group_name}/Rezult_{group_name}.txt", "w", encoding='utf-8') as file_end:
            file_end.write("ничего криминального")


def comment(group_name,word_comment):
    
    b = 0
    l = []
    with open(f"{group_name}/exist_posts_{group_name}.txt") as f:
        l = f.read().splitlines()
    for i in l:
        with io.open(f"{group_name}/text_comment{i}_{group_name}.txt", encoding='utf-8') as file:
            
            for line in file:
                if word_comment in line:
                    b += 1
        if b != 0:
            with open(f"{group_name}/Rezult_comment_{group_name}.txt", "w", encoding='utf-8') as file_end:
                file_end.write("не подходит")
        else:
            with open(f"{group_name}/Rezult_comment_{group_name}.txt", "w", encoding='utf-8') as file_end:
                file_end.write("ничего криминального")

def main(group_name, word_group, word_comment):
    group(group_name,word_group)
    comment(group_name,word_comment)

if __name__ == '__main__':
    main()