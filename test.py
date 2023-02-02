#!/bin/python3

# > by Edouard

# Edited by Paul Parisot, edit not approved by Edouard

import glob
import os
import time
import threading
import sys

bin = "bsq"

solved_maps = "seemouli/maps-intermediate/mouli_maps_solved"
tested_maps = "seemouli/maps-intermediate/mouli_maps"

solved_inputs = "seemouli/inputs/solved"
tested_inputs = "seemouli/inputs/tested.txt"

tmp = "seemouli/tmp"
testname = "test-"

timeout = 15

################################""

map_list = [i [len(tested_maps) +1 ::] for i in glob.glob(f"{tested_maps}/*")]
testL = [None for i in range(len(map_list))]

class c:
    reset = "\033[m"
    bold = "\033[1m"
    under = "\033[4m"

    red = "\033[31m"
    blue = "\033[94m"
    green = "\033[92m"
    orange = "\033[33m"


def write_in(verb: str, n: int, ret: bool):
    with open(f"{tmp}/log.txt", "a") as f:
        f.write(verb)

    testL[n] = ret
    os.remove(f"{tmp}/{testname}{n}.txt")
    return ret


def test(map, n) :
    global testL
    verb = ""

    if os.path.exists(f"{tmp}/{testname}{n}.txt"):
        os.remove(f"{tmp}/{testname}{n}.txt")
    bt = time.time()
    e = os.system(f"timeout {timeout + 3} ./{bin} {tested_maps}/{map} > {tmp}/{testname}{n}.txt")

    if time.time() - bt > timeout :
        print(f"{c.orange}[T]{c.reset}\t {map}")
        verb += f"Failed : {map} (timeout)\n"
        return write_in(verb, n, False)
        
    if e != 0:
        print(f"{c.red}[C]{c.reset}\t {map}")
        verb += f"Failed : {map} (crashed)\n"
        return write_in(verb, n, False)
    
    if open(f"{solved_maps}/{map}", "r").read() == open(f"{tmp}/{testname}{n}.txt", "r").read() :
        print(f"{c.green}[S]{c.reset}\t {map}")
        verb += f"Passed : {map}\n"
        return write_in(verb, n, True)

    else:
        print(f"{c.red}[F]\t {c.under}{map}{c.reset}")
        verb += f"Failed : {map}\n"
        verb += "Expected:\n"
        verb += open(f"{solved_maps}/{map}", "r").read()
        verb += "Got:\n"
        verb += open(f"{tmp}/{testname}{n}.txt", "r").read()
        return write_in(verb, n, False)

def normal_tests():
    if os.path.exists(f"{tmp}/log.txt") :
        os.remove(f"{tmp}/log.txt")

    for i in range(len(map_list)) :
        threading.Thread(target=test, args=(map_list[i], i)).start()

        
    while threading.active_count() > 1 :
        time.sleep(0.1)

    total = 0
    for i in range(len(map_list)) :
        if testL[i] == True :
            total += 1

    trash = [i for i in glob.glob("{tmp}/{testname}*.txt")]
    for i in trash:
        os.remove(i)
    
    return f"\n{round(total/len(map_list)*100)}% normal tests passed ({total}/{len(map_list)})"


def input_tests():
    table = open(tested_inputs, "r").read().split('\n')
    total = 0

    for i in range(len(table)):
        index = i + 1
        os.system(f"timeout {timeout} {table[i]} > {tmp}/{testname}{index}")

        my_solved = open(f"{solved_inputs}/{index}", "r").read()
        my_test = open(f"{tmp}/{testname}{index}", "r").read()
        if my_solved == my_test:
            print(f"{c.green}[S]{c.reset}\t {table[i]}")
            total += 1
        else:
            print(f"{c.red}[F]\t {c.under}{table[i]}{c.reset}")

    return f"{round(total/len(table)) * 100}% input tests passed ({total}/{len(table)})\n"


if __name__ == "__main__":

    if len(sys.argv) > 1 :
        bin = sys.argv[1]

    os.system("make re | printf \"\"")
    os.system("make clean | printf \"\"")

    normal_test_result = normal_tests()
    print()
    input_test_result = input_tests()

    print(normal_test_result)
    print(input_test_result)