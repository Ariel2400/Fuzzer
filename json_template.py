from dataclasses import dataclass
from typing import TypeVar, Generic
from enum import Enum
from uu import decode
import random as rand
import re
import pyjson5
import random

T = TypeVar('T')


class Endian(Enum):
    BIG = 1
    LITTLE = 2


class Format(Enum):
    NULL_TERMINATED = 1


# random: bool, size: int = None, val: T = None, endian: Endian = None, isBits: bool = False,
# format_string: Format = None
@dataclass
class GrammarType(Generic[T]):
    random: bool
    size: int = 0
    val: T = None
    endian: Endian = None
    isBits: bool = False

    # if format string: format string && val
    # if random: isBits? random byte (size) times :


class GrammarTemplate:
    def __init__(self, arrayOfGrammarValues: list[GrammarType]):
        self.arrayOfGrammarValues = arrayOfGrammarValues

    @staticmethod
    def computeGrammarFunction(json_string, function_string):
        function_string = function_string.replace(' ', '')

        if function_string.isnumeric():
            return int(function_string)

        signature = function_string.split(':', 1)[0]
        body = function_string.split(':', 1)[1]

        compute_val = None

        if signature == 'add':
            elements = re.split(r',(?!(?:[^(]*\([^)]*\))*[^()]*\))', body[1:-1])
            sum = 0
            for element in elements:
                sum += GrammarTemplate.computeGrammarFunction(json_string, element)
            compute_val = sum

        elif signature == 'size':
            block = body[1:-1]
            compute_val = json_string[block]["size"]

        return compute_val

    @staticmethod
    def createGrammarTemplateOfBlock(size=None, data=None, endian=None, isBits=False):
        arrayGrammarValues = []

        if not data:
            arrayGrammarValues += [GrammarType(random=True, size=size, isBits=isBits)]
        elif type(data) == int:
            endian_form = Endian.LITTLE
            if endian:
                endian_form = endian
            arrayGrammarValues += [GrammarType(random=False, size=size, val=data, endian=endian_form, isBits=isBits)]
        elif type(data) == str:
            if size > len(data):
                arrayGrammarValues += [GrammarType(random=False, size=len(data), val=data, isBits=isBits)]
                arrayGrammarValues += [GrammarType(random=True, size=size - len(data), isBits=isBits)]
            else:
                arrayGrammarValues += [GrammarType(random=False, size=size, val=data, isBits=isBits)]

        return arrayGrammarValues

    @staticmethod
    def createGrammarTemplateFromJsonString(json_string, start_block):
        arrayGrammarValues = []

        # byte_block
        if json_string[start_block]["type"] == "byte_block":
            data = None
            endian = None
            if "data" in json_string[start_block]:
                data = json_string[start_block]["data"]
            elif "data-func" in json_string[start_block]:
                data = GrammarTemplate.computeGrammarFunction(json_string, json_string[start_block]["data-func"])
            if "endian" in json_string[start_block]:
                endian = json_string[start_block]["endian"]
            arrayGrammarValues += GrammarTemplate.createGrammarTemplateOfBlock(size=json_string[start_block]["size"],
                                                                               data=data, endian=endian)

        # range_byte_block
        elif json_string[start_block]["type"] == "range_byte_block":
            data = None
            endian = None
            range = json_string[start_block]["range"]
            size = random.randint(range[0], range[1])
            if "data" in json_string[start_block]:
                data = json_string[start_block]["data"]
            elif "data-func" in json_string[start_block]:
                data = GrammarTemplate.computeGrammarFunction(json_string, json_string[start_block]["data-func"])
            if "endian" in json_string[start_block]:
                endian = json_string[start_block]["endian"]
            arrayGrammarValues += GrammarTemplate.createGrammarTemplateOfBlock(size=size, data=data, endian=endian)

        # str_block
        elif json_string[start_block]["type"] == "str_block":
            arrayGrammarValues += GrammarType(random=False, format_string=json_string[start_block]["format"],
                                              val=json_string[start_block]["content"])

        # multi_bit_block
        elif json_string[start_block]["type"] == "multi_bit_block":
            bit_blocks = json_string[start_block]["bit_blocks"]
            for bit_block in bit_blocks:
                data = None
                if data in json_string[bit_block]:
                    data = json_string[bit_block]["data"]
                arrayGrammarValues += GrammarTemplate.createGrammarTemplateOfBlock(size=json_string[bit_block]["size"],
                                                                                   data=data, isBits=True)

        # multi_byte_block
        elif json_string[start_block]["type"] == "multi_byte_block":
            byte_blocks = json_string[start_block]["byte_blocks"]
            for byte_block in byte_blocks:
                arrayGrammarValues += GrammarTemplate.createGrammarTemplateFromJsonString(json_string, byte_block)

        # duplicate_block
        elif json_string[start_block]["type"] == "duplicate_block":
            size = json_string[start_block]["size"]
            block = json_string[start_block]["block"]
            blockTemplate = GrammarTemplate.createGrammarTemplateFromJsonString(json_string, block)
            arrayGrammarValues += blockTemplate * size

        # range_duplicate_block
        elif json_string[start_block]["type"] == "range_duplicate_block":
            block = json_string[start_block]["block"]
            range = json_string[start_block]["range"]
            size = random.randint(range[0], range[1])
            blockTemplate = GrammarTemplate.createGrammarTemplateFromJsonString(json_string, block)
            arrayGrammarValues += blockTemplate * size

        # choice_block
        elif json_string[start_block]["type"] == "choice_block":
            blocks = json_string[start_block]["blocks"]
            arrayGrammarValues += GrammarTemplate.createGrammarTemplateFromJsonString(json_string,
                                                                                      random.choice(blocks))

        return arrayGrammarValues

    @staticmethod
    def createGrammarTemplateFromFile(jsonFileName):
        objFile = open(jsonFileName, 'r')
        decoded_json = pyjson5.decode_io(objFile, None, False)
        if "main_template" not in decoded_json:
            print("dont have main_template block!")
            return

        return GrammarTemplate(GrammarTemplate.createGrammarTemplateFromJsonString(decoded_json, "main_template"))

    def create_file(self, path):
        with open(path, 'wb') as f:
            buffer = b''
            for i, element in enumerate(self.arrayOfGrammarValues):
                if element.random and not element.isBits:
                    f.write(random.randbytes(element.size))
                elif element.random and element.isBits and len(buffer) % 8 != 0:
                    buffer.join([random.choice([b'1', b'0']) for _ in range(element.size)])
                elif element.endian == Endian.LITTLE:
                    f.write(element.val.to_bytes(element.size, 'little'))
                elif element.endian == Endian.BIG:
                    f.write(element.val.to_bytes(element.size, 'big'))
                else:
                    f.write(str(element.val)[:element.size].encode())
                    print(f"element[{i}] out of {len(self.arrayOfGrammarValues)} : {element}")


if __name__ == '__main__':
    t = GrammarTemplate.createGrammarTemplateFromFile("bmp.json5")
    # print(t.arrayOfGrammarValues)
    # temp = GrammarTemplate(arr)
    t.create_file('check3.bmp')
    i = 0
    # for grammarInstance in template.arrayOfGrammarValues:
    #     print("random = ", grammarInstance.random)
    #     print("size = ", grammarInstance.size)
    #     print("val = ", grammarInstance.val)
    #     print("endian = ", grammarInstance.endian)
    #     print("isBits = ", grammarInstance.isBits)
    #     print("format_string = ", grammarInstance.format_string)
    #     print("\n\n")
    #     if i == 8:
    #         break
    #     i += 1
