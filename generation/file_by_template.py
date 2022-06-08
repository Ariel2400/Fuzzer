import jsonschema
import string
from typing import TypeVar, Generic
from enum import Enum
import random
import re
import pyjson5
import random
from dataclasses import dataclass

#from database.my_producer import MyProducer

T = TypeVar('T')


def strToBytes(string):
    stringBytes = []
    for ch in string:
        stringBytes += [ord(ch)]
    return bytes(stringBytes)


def validateJson(jsonData, schema):
    try:
        jsonschema.validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


class Endian(Enum):
    BIG = 0
    LITTLE = 1


@dataclass
class GrammarType(Generic[T]):
    random: bool
    val: T = None
    format_string: str = 'c-string'
    endian: Endian=Endian.LITTLE
    isBits: bool = False
    size: int = 0


class GrammarTemplate:
    JSON_SCHEMA_PATH = 'grammar-schema.json'

    def __init__(self, arrayOfGrammarValues: list):
        self.arrayOfGrammarValues = arrayOfGrammarValues
        # self.kafkaProducer = MyProducer()
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

        if data is None:
            arrayGrammarValues += [GrammarType(random=True, size=size, isBits=isBits)]
        elif type(data) == int:
            endian_form = Endian.LITTLE
            if endian is not None:
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
            range_array = json_string[start_block]["range"]
            size = random.randint(range_array[0], range_array[1])
            if "data" in json_string[start_block]:
                data = json_string[start_block]["data"]
            elif "data-func" in json_string[start_block]:
                data = GrammarTemplate.computeGrammarFunction(json_string, json_string[start_block]["data-func"])
            if "endian" in json_string[start_block]:
                endian = json_string[start_block]["endian"]
            arrayGrammarValues += GrammarTemplate.createGrammarTemplateOfBlock(size=size, data=data, endian=endian)

        # str_block
        elif json_string[start_block]["type"] == "str_block":
            arrayGrammarValues.append(GrammarType(random=False,
                                                  format_string=json_string[start_block]["format"],
                                                  val=json_string[start_block]["content"],
                                                  size=len(json_string[start_block]['content'])))

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
            size = int(json_string[start_block]["size"])
            block = json_string[start_block]["block"]
            for _ in range(size):
                arrayGrammarValues += GrammarTemplate.createGrammarTemplateFromJsonString(json_string, block)
            

        # range_duplicate_block
        elif json_string[start_block]["type"] == "range_duplicate_block":
            block = json_string[start_block]["block"]
            range_array = json_string[start_block]["range"]
            size = random.randint(int(range_array[0]), int(range_array[1]))
            for _ in range(size):
                arrayGrammarValues += GrammarTemplate.createGrammarTemplateFromJsonString(json_string, block)
            

        # choice_block
        elif json_string[start_block]["type"] == "choice_block":
            blocks = json_string[start_block]["blocks"]
            arrayGrammarValues += GrammarTemplate.createGrammarTemplateFromJsonString(json_string,
                                                                                      random.choice(blocks))

        return arrayGrammarValues

    @staticmethod
    def createGrammarTemplateFromFile(jsonFileName):
        objFileJson = open(jsonFileName, 'r')
        objFileSchema = open(GrammarTemplate.JSON_SCHEMA_PATH, 'r')
        decoded_json = pyjson5.decode_io(objFileJson, None, False)
        decoded_schema = pyjson5.decode_io(objFileSchema, None, False)
        if(not validateJson(decoded_json, decoded_schema)):
            raise Exception("Schema validation failed!")
        if ("main_template" not in decoded_json):
            raise Exception("dont have main_template block!")

        return GrammarTemplate(GrammarTemplate.createGrammarTemplateFromJsonString(decoded_json, "main_template"))

    def create_file(self, path):
        buffer = b''
        
        chars = string.punctuation + string.digits + string.ascii_letters
        for element in self.arrayOfGrammarValues:
            if element.random:
                val = ''.join(random.choice(chars) for i in range(element.size))
                buffer += strToBytes(val)
            else:
                if type(element.val) == str:
                    val = element.val
                    if len(val) > element.size:
                        val = val[:element.size]
                    buffer += strToBytes(val)
                elif type(element.val) == int:
                    endian = 'little'
                    if element.endian == Endian.BIG:
                        endian = 'big'
                    val = element.val.to_bytes(element.size, endian)
                    buffer += strToBytes(val)
        with open(path, 'wb') as f:
            f.write(buffer)
        #self.kafkaProducer.send_file(buffer)
    
    def close_kafka(self):
        self.kafkaProducer.close()



if __name__ == "__main__":
    
    for i in range(1_000_000):
        try:
            print(f'writing {i}/10000')
            obj = GrammarTemplate.createGrammarTemplateFromFile("./grammar_for_json.json5")
            obj.create_file(f"./jsons/{i}.json")
        except RecursionError:
            continue