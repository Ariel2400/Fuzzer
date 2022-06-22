
## Usage/Examples

The first argument is the technique in which you want to perform fuzzing(mutation, Generation, symbolic_execution).
Each technique has optional and necessary arguments relevant to it.
### General Arguments
 - target - target for fuzzing(required)
 - target_args - command line arguments of target(optional)
 - crashes_dir_path - crashes_dir_path for fuzzing crashes(required)
 - fuzz_amount - cycles of fuzzing(optional, if not specify The fuzzing will be endless)
 - threads_number - number of threads that will be fuzz in parallel(optional, if not specify the number will be 2 * (number of cores))
 - stdin_input - throw input to target's stdin(optional, if not specify the input will be thrown as file argument)

### Mutation

 - sample_dir_path - samples for mutation directory(required)


```python
python3 ./src/run.py mutation --target /usr/bin/objdump --target_args " -d" --sample_dir_path ./samples_test --crashes_dir_path ./crashes
```

### Generation

 - grammar_file_path - grammar for generating samples(required)
 - mutation_number - do mutation_number number of mutation on generated data(optional, if not specify there will not be mutation)

```python
python3 ./src/run.py generation --target /bin/jq --target_args ". " --crashes_dir_path ./ --grammar_file_path ./src/generation/grammar_for_json.json5 --mutation 10
```

### Symbolic Execution

 - len_symbolic_bytes - target input len symbolic bytes(required)
 - load_dynamic_libaries - load dynamic libaries for symbolic execution(optional)
 - use_kafka - use kafka for delivering messages to fuzzer(optional, To use you need to run kafka first)

```python
python3 ./src/run.py symbolic_execution --target ../../code/a.out --target_args "flag1" --crashes_dir_path ./crashes_test --len_symbolic_bytes 5 --fuzz_amount 100 --stdin
```
