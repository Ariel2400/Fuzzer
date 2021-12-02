import mutations

class SimpleFuzzer:
    


# create a new file with sample_content and run it on the target_command_line 
def fuzz(thr_id, sample_content, target_command_line, crashes_dir, sample_file_name):
    assert isinstance(thr_id, int)
    assert isinstance(sample_content, bytearray)
    assert isinstance(target_command_line, list)
    pass