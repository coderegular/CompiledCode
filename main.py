import re


# This function will give you Primary inputs
def find_pi_po(li):
    my_inputs = []
    my_outputs = []

    for j in li:
        x = re.findall('[a-z]', j)
        if len(x) == 3:
            my_inputs.append(x[1:])
            my_outputs.append(x[0])
        elif len(x) == 2:
            my_inputs.append(x[-1])
            my_outputs.append(x[0])
    my_po = []
    for i in range(len(my_outputs)):
        flag = False
        for j in my_inputs:
            if my_outputs[i] in j:
                flag = True
                break
        if not flag and my_outputs[i] not in my_po:
            my_po.append(my_outputs[i])

    for o in my_outputs:
        for i in my_inputs:
            if o in i:
                i.remove(o)

    my_pi = []
    for i in range(len(my_inputs)):
        for j in range(len(my_inputs[i])):
            if my_inputs[i][j] not in my_pi:
                my_pi.append(my_inputs[i][j])

    return my_pi, my_po


# This function will give you all operation
def get_op(li):
    my_op_list = []
    for l in li:
        x = re.findall('[A-Z]', l)
        n = ""
        for j in x:
            n += j
        my_op_list.append(n)
    return my_op_list


# this function will extract all wires
def get_all_wire(li):
    all_wire = []
    for i in li:
        temp = re.findall('[a-z]', i)
        for j in temp:
            if j not in all_wire:
                all_wire.append(j)
    return all_wire


def my_xor(d, b):
    return (not d) & b or d & (not b)


with open('sample.vh') as my_file:
    content = my_file.readlines()
    content_list = []
    for row in content:
        content_list.append(row.strip())

# all wires are listed in wires_list
wires_list = get_all_wire(content_list)
OP_list = get_op(content)
my_pi, my_po = find_pi_po(content_list)

# Initialization
level = []
for i in wires_list:
    if i not in my_pi:
        level.insert(wires_list.index(i), 'x')
    else:
        level.insert(wires_list.index(i), 0)

dic_op = {}
counter = 1
for i in OP_list:
    a = "a" + str(counter)
    counter += 1
    dic_op[a] = i

val_dic = {}
cnt = 1
for i in content_list:
    a = "a" + str(cnt)
    cnt += 1
    temp = re.findall('[a-z]', i)
    val_dic[a] = temp

# make queue for the gates
my_queue = list(dic_op.keys())

# Determine Leve of each wire
level_counter = 0
while len(my_queue) and level_counter != 2 * len(dic_op):
    t = my_queue.pop(0)
    ws = val_dic[t][1:]
    if len(ws) > 1:
        if (level[wires_list.index(ws[0])] != 'x') & (level[wires_list.index(ws[1])] != 'x'):
            level[wires_list.index(val_dic[t][0])] = max(level[wires_list.index(ws[0])],
                                                         level[wires_list.index(ws[1])]) + 1
        else:
            my_queue.insert(len(my_queue), t)
            level_counter = level_counter + 1
    else:
        if level[wires_list.index(ws[0])] != 'x':
            level[wires_list.index(val_dic[t][0])] = level[wires_list.index(ws[0])] + 1
        else:
            my_queue.insert(len(my_queue), t)
            level_counter = level_counter + 1

if level_counter == 2 * len(dic_op):
    print("*"*50)
    print("circuit is unstable")
    print("*" * 50)
else:
    dict_level = {}
    for i in val_dic:
        temp = val_dic[i]
        out = temp[0]
        dict_level[i] = level[wires_list.index(out)]

    dict_level = sorted(dict_level.items(), key=lambda x: x[1])
    output_of_every_gate = []
    for i in wires_list:
        output_of_every_gate.append("x")

    for i in my_pi:
        output_of_every_gate[wires_list.index(i)] = int(input(f"please enter value of {i}:"))

    for i in dict_level:
        if dic_op[i[0]] == "AND":
            if output_of_every_gate[wires_list.index(val_dic[i[0]][1])] & \
                    output_of_every_gate[wires_list.index(val_dic[i[0]][2])]:
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 1
            else:
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 0
        elif dic_op[i[0]] == "OR":
            if (output_of_every_gate[wires_list.index(val_dic[i[0]][1])]) or (
                    output_of_every_gate[wires_list.index(val_dic[i[0]][2])]):
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 1
            else:
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 0

        elif dic_op[i[0]] == "NOT":
            if not output_of_every_gate[wires_list.index(val_dic[i[0]][1])]:
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 1
            else:
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 0
        elif dic_op[i[0]] == "NAND":
            if not (output_of_every_gate[wires_list.index(val_dic[i[0]][1])] &
                    output_of_every_gate[wires_list.index(val_dic[i[0]][2])]):
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 1
            else:
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 0
        elif dic_op[i[0]] == "NOR":
            if not (output_of_every_gate[wires_list.index(val_dic[i[0]][1])] |
                    output_of_every_gate[wires_list.index(val_dic[i[0]][2])]):
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 0
            else:
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 1
        elif dic_op[i[0]] == "XOR":
            if my_xor(output_of_every_gate[wires_list.index(val_dic[i[0]][1])],
                      output_of_every_gate[wires_list.index(val_dic[i[0]][2])]):
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 1
            else:
                output_of_every_gate[wires_list.index(val_dic[i[0]][0])] = 0

# print outputs
    print("*"*70)
    print(f"The primary inputs are : {my_pi}")
    print(f"The primary outputs are : {my_po}")
    for i in my_po:
        print(f"The output of {i} is {output_of_every_gate[wires_list.index(i)]}")
    for i in dic_op:
        print(f"The level of {dic_op[i]} gate is : {level[wires_list.index(val_dic[i][0])]}")
    print(f"the levels are : {level}")
    ans = input("If you want to see every wires value type yes :")
    if ans.lower().startswith('y'):
        for i in wires_list:
            print(f'The value of wire {i} is {output_of_every_gate[wires_list.index(i)]}')
    print("*" * 70)
