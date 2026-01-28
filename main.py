import json
import os
import sys
from dataclasses import dataclass, asdict

if len(sys.argv) == 1:
    print("Waiting for response...")
    os.system("wget -q --show-progress https://scibowldb.com/api/questions")
    print("Done.")
    os.system("mv questions questions.json")
print("Reading...")
f = open("questions.json", "r")
jsondata = f.read()
f.close()
data = json.loads(jsondata)["questions"]
jsondata = False
physics: list[dict] = []
general_science = []
energy = []
earth_space =[]
earth_science = []
chemistry = []
biology = []
astronomy = []
math = []
computer_science = []
print("Looping...")
for i in data:
    append = True
    match i["category"]:
        case "PHYSICS":
            qlist = physics
        case "GENERAL SCIENCE":
            qlist = general_science
        case "ENERGY":
            qlist = energy
        case "EARTH AND SPACE":
            qlist = earth_space
        case "EARTH SCIENCE":
            qlist = earth_science
        case "CHEMISTRY":
            qlist = chemistry
        case "BIOLOGY":
            qlist = biology
        case "ASTRONOMY":
            qlist = astronomy
        case "MATH":
            qlist = math
        case "COMPUTER SCIENCE":
            qlist = computer_science
        case _:
            print("Unkown category:", i["category"])
            append = False
    if append:
        qlist.append(i)
print("Writing topics")
f = open("physics.json", "w")
f.write(json.dumps(physics, indent=4))
f.close()
f = open("general science.json", "w")
f.write(json.dumps(general_science, indent=4))
f.close()
f = open("energy.json", "w")
f.write(json.dumps(energy, indent=4))
f.close()
f = open("earth and space.json", "w")
f.write(json.dumps(earth_space, indent=4))
f.close()
f = open("earth science.json", "w")
f.write(json.dumps(earth_science, indent=4))
f.close()
f = open("chemistry.json", "w")
f.write(json.dumps(chemistry, indent=4))
f.close()
f = open("biology.json", "w")
f.write(json.dumps(biology, indent=4))
f.close()
f = open("astronomy.json", "w")
f.write(json.dumps(astronomy, indent=4))
f.close()
f = open("math.json", "w")
f.write(json.dumps(math, indent=4))
f.close()
f = open("computer science.json", "w")
f.write(json.dumps(computer_science, indent=4))
f.close()

@dataclass
class Packet:
    name: str
    number: int

@dataclass
class Set:
    name: str
    year: int
    standard: bool

@dataclass
class tossup:
    question: str
    question_sanitized: str
    answer: str
    answer_sanitized: str
    category: str
    subcategory: str
    packet: Packet
    set: Set

physics_tossups: list[dict] = []

i: dict
for i in physics:
    question = ""
    if i["source"][:12] != "Official-set":
        continue
    if i["tossup_format"] == "Multiple Choice":
        l: list[str] = i["tossup_question"].split("\n")
        for j in l:
            question += j + "<br />"
    else:
        question = i["tossup_question"]
    prefix = "Tossup " + "Physics " + i["tossup_format"]
    formattedAnswer = ""
    if i["tossup_format"] == "Multiple Choice":
        l: list[str] = i["tossup_answer"].split(")")
        if len(l) == 1:
            print("Warning: Multiple choice question without `)'. Question is", i["id"], "Answer is", i["tossup_answer"])
            l: list[str] = i["tossup_answer"].split("--")
            if len(l) == 1:
                print("Error: Could not resolve issue")
                continue
            formattedAnswer = "<b><u>" + l[0] + "</u></b>" + " (Accept " + "<b><u>" + l[1].title() + "</u></b>)"
            continue
        formattedAnswer = "<b><u>" + l[0] + "</u></b>" + " (Accept " + "<b><u>" + l[1].title() + "</u></b>)"
    else:
        formattedAnswer = "<b><u>" + i["tossup_answer"] + "</u></b>"
    physics_tossups.append(asdict(tossup(
        "<b>" + prefix + " " + question + " (*) </b>",
        prefix + " " + question.replace("<br />", " \n"),
        formattedAnswer,
        i["tossup_answer"],
        "Science",
        "Physics",
        Packet(i["source"], int(i["source"].split("round")[1])),
        Set("2000" + i["source"], 2000, False)
    )))

f = open("qbreader.json", "w")
f.write(json.dumps({"tossups":physics_tossups,"bonuses":[]}, indent=4))
f.close()