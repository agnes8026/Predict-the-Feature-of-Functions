import random
import re
import os

def remove_up_to_first_hex(lst):
    pattern = r'^[0-9a-fA-F]{8}$'
    for index, item in enumerate(lst):
        if re.match(pattern, item):
            del lst[index]
            return

def delete_items(line):
    items = line.split()
    remove_up_to_first_hex(items)
    output = []
    for i in range(len(items)):
        output.append(items[i])

    return ' '.join(output)

def mask_instruction(instruction, mask_prob):
    masked_instruction = []
    skip_next = False

    for i, token in enumerate(instruction):
        if skip_next:
            skip_next = False
            continue

        if "*" in token:
            skip_next = True
        else:
            if random.random() < mask_prob:
                masked_instruction.append("[MASK]")
            else:
                masked_instruction.append(token)

    return " ".join(masked_instruction)

file_path = "strip_7.txt"
# output_path = "strip_7_output.txt"
# mask_path = "strip_mask.txt"
# folder_path = "functionextraction"
# mask_prob = 0.10

# for file_name in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, file_name)

#     if not os.path.isfile(file_path):
#         continue

with open(file_path, 'r') as file:
    lines = file.readlines()

masked_instructions = []
original_instructions = []

for line in lines:
    line = line.strip()
    if line == "":
        continue
    result_line = delete_items(line)
    instruction = result_line.split(" ")
    original_instructions.append(" ".join(instruction))
    # masked_instruction = mask_instruction(instruction, mask_prob)
    # masked_instructions.append(masked_instruction)

# masked_file_path = os.path.join(folder_path + "\\maskedfile", f"masked_{file_name}")
# output_file_path = os.path.join(folder_path + "\\outputfile", f"modified_{file_name}")
output_file_path = "strip_7_labeled.txt"
# with open(masked_file_path, 'w') as file:
    # file.write("\n".join(masked_instructions))
with open(output_file_path, 'w') as file:
    file.write("\n".join(original_instructions))