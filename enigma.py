# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError
from pickle import SETITEM
from tkinter import E

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
start=True
WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])
    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))
    
    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input

# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]

# Wheels
def pass_wheels(input, reverse = False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order

    if not reverse :
        # 세번째 휠 통과
        index = ETW.find(input)
        input = SETTINGS["WHEELS"][2]["wire"][index]

        # 두번째 휠 통과
        index = ETW.find(input)
        input = SETTINGS["WHEELS"][1]["wire"][index]

        # 첫번째 휠 통과
        index = ETW.find(input)
        input = SETTINGS["WHEELS"][0]["wire"][index]

    else:
        # 첫번째 휠 통과
        index = SETTINGS["WHEELS"][0]["wire"].find(input)
        input = ETW[index]

        # 두번째 휠 통과
        index = SETTINGS["WHEELS"][1]["wire"].find(input)
        input = ETW[index]

        # 세번째 휠 통과
        index = SETTINGS["WHEELS"][2]["wire"].find(input)
        input = ETW[index]
    return input

# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics
    global start
    #초기화 알고리즘
    if  start:
        start = False
        for _ in range(SETTINGS["WHEEL_POS"][0]):
            SETTINGS["WHEELS"][0]["wire"] =  SETTINGS["WHEELS"][0]["wire"][1:26] + SETTINGS["WHEELS"][0]["wire"][0] 
        for _ in range(SETTINGS["WHEEL_POS"][1]):
            SETTINGS["WHEELS"][1]["wire"] =  SETTINGS["WHEELS"][1]["wire"][1:26] + SETTINGS["WHEELS"][1]["wire"][0] 
        for _ in range(SETTINGS["WHEEL_POS"][2]):
            SETTINGS["WHEELS"][2]["wire"] =  SETTINGS["WHEELS"][2]["wire"][1:26] + SETTINGS["WHEELS"][2]["wire"][0] 

        # print("초기화 "+ SETTINGS["WHEELS"][0]["wire"])
        # print("초기화 "+ SETTINGS["WHEELS"][1]["wire"])
        # print("초기화 "+ SETTINGS["WHEELS"][2]["wire"])
    

    #회전하는 타이밍 저장
    wheel_I_turn    = SETTINGS["WHEELS"][0]["wire"][(SETTINGS["WHEELS"][0]['turn'])]
    wheel_II_turn   = SETTINGS["WHEELS"][1]["wire"][(SETTINGS["WHEELS"][1]['turn'])]

    #회전 구현
    SETTINGS["WHEELS"][0]["wire"] =  SETTINGS["WHEELS"][0]["wire"][1:26]+ SETTINGS["WHEELS"][0]["wire"][0]
    if wheel_I_turn == SETTINGS["WHEELS"][0]['wire'][0]:
        SETTINGS["WHEELS"][1]["wire"] =  SETTINGS["WHEELS"][1]["wire"][1:26] + SETTINGS["WHEELS"][1]["wire"][0]

        if wheel_II_turn == SETTINGS["WHEELS"][1]['wire'][0]:
            SETTINGS["WHEELS"][2]["wire"] =  SETTINGS["WHEELS"][2]["wire"][1:26] + SETTINGS["WHEELS"][2]["wire"][0]
    
    # print("회전 : ",SETTINGS["WHEELS"][0]["wire"])
    # print("회전 : ",SETTINGS["WHEELS"][1]["wire"])
    # print("회전 : ",SETTINGS["WHEELS"][2]["wire"])

# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True)
    encoded_ch = pass_plugboard(encoded_ch)


    print(encoded_ch, end='')
