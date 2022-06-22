# Grammar

In order to generate files in the desired format, You need to a grammar to that format first. 

The grammar is written as a json file and built from grammar blocks, which are json objects with defined properties.

the basic block looks like this:
```
"block_identifier" : {
    "type": "block_type",
    "additional properties":"values",
}
```

here's the list of the blocks:
## Byte block
The byte block is a block that represents a chunk of bytes. It can be specific or randomly generated.
its fields are: 
- `"type"`: must always be `"byte_block"`
 - `"size"`: the size of the desired data to be generated, in bytes. Given as an integer.
 - `"data"`: the data that you want the block to have. if the actual size of the data is smaller than the one specified in the `"data"` field than the rest will fill up with random bytes. leave empty to get random data. the data must be given as an integer or a string
 - `"endian"`: must be `"big"` or `"little"`. `"little"` is the default 
 
 examples:
 ```
 "field_1" : {
        "type" : "byte_block",
        "size" : 4,
        "data" : 43
    },

    "field_2" : {
        "type" : "byte_block",
        "size" : 4,
        "data" : "oo", //last two bytes will be random, as each char takes ine byte
    },
 ```

 ## Range byte block
 The range byte block duplicates the value it's given as bytes between a minimum and maximum number of times.
 - `"type"`: must be always `"range_block"`
 - `"range"`: the size of the block, given as a list of a minimum integer and maximum. so that for example if `"range":[1, 4]`, then the data will be duplicated for any number of times between 1 and 4.
 - `"data"`: the data you wish to duplicate, can be an integer or a string. if left empty it will be generated randomly
 - `"endian"`: must be `"big"` or `"little"`. `"little"` is the default

 examples:
 ```
 "range_example":{
    "type": "range_block",
    "range: [1,4],
    "data": 42,
    "endian":"big"
 }
 ```

 ## String block
 A block that represents a string.
 - `"type"`: must be always `"str_block"`
 - `"content"`: the string itself. must be filled.
 - `"format"`: either `"c-string"` or `"pascal-string"`

 examples:
 ```
 "field_3" : {
        "type" : "str_block",
        "content" : "Hello",
        "format" : "c-string" // with null in the end
}
```

## Bit block
A block that represents a chunk of bits(not to be confused with bytes).
- `"type"`: must be always `"bit_block"`
- `"size"`: the size of the desired data to be generated, in bits. Given as an integer.
- `"data"`: the data that you want the block to have. if the actual size of the data is smaller than the one specified in the `"data"` field than the rest will fill up with random bites. leave empty to get random data. the data must be given as a string

example: 
```
"bit_example":{
    "type" : "bit_block",
    "size" : "5",
    "data" : "01110"
}
```
##  Multi-Bit block
Concatenation of multiple bit blocks
 - `"type"`: must be always `"multi_bit_block"`
 - `"bit_blocks"`: list of `bit blocks` that will be concatenated (total size must be divisible by 8)

 example:
 ```
  "multi_name" : {
        "type" : "multi_bit_block",
        "bit_blocks" : ["some_bits1", "some_bits2"] 
    }
 ```

 ## Multi-Byte block
 same as `multi bit block`, but with bytes. 
  - `"type"`: must be always `"multi_byte_block"`
 - `"byte_blocks"`: list of `byte blocks` that will be concatenated

 example:
 ```
 "multi_bytes" : {
    "type": "multi_byte_block",
    "byte_blocks": ["byte_block_a", "byte_block_b"]
 }
 ```

 # Duplicate block
 duplicates a given grammar block
 - `"type"`: must be always `"duplicate_block"`
 - `"block"`: the block you wish to duplicate. note that if it's a random block, it will generate the data each iteration. no `bit block` allowed
 - `"size"`: the number of duplications, an integer

 example:
 ```
 "duplicate_example":{
    "type": "duplicate_block",
    "block": "some_block",
    "size": 3
 }
```

## Range duplicate block
same as `duplicate block` but the number of duplications is random between a min and max.
- `"type"`: must be always `"range_duplicate_block"`
 - `"block"`: the block you wish to duplicate. note that if it's a random block, it will generate the data each iteration. no `bit block` allowed
 - `"range"`: a list where the first element is the min number of duplications and the second is the max

 example:
 ```
 "duplicate_example":{
    "type": "range_duplicate_block",
    "block": "some_block",
    "size": [0, 10]
 }
```

## Choice block
chooses a block randomly from a list of blocks
- `"type"`: must be always `"range_duplicate_block"`
- `"blocks"`: a list of blocks from which one is chosen randomly

example: 
```
"choice_example":{
    "type": "choice_block",
    "blocks":["some_block1", "some_block2"]
}
```
