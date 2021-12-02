use std::io;
use std::os::unix::prelude::ExitStatusExt;
use std::path::Path;
use std::fs;
use std::process::{Command, ExitStatus};
use std::thread;
use std::time;
use std::collections::BTreeSet;
use::std::sync;
use rand::Rng;
use std::env;

//number of uterations per thread before computing statistics
const BATCH_SIZE: usize = 100;

//Write file_data to file and execute the target on the file
fn fuzz(file_path: &Path, file_data: &[u8], target_and_arguments: &sync::Arc<Vec<String>>) -> Result<ExitStatus, io::Error>{
    //write data to file
    fs::write(file_path, file_data)?;

    //execute the target on file
    let output = Command::new(&target_and_arguments.as_ref()[0]).args([&target_and_arguments.as_ref()[1..], &[String::from(file_path.to_str().unwrap())]].concat()).output()?;
    //return status code
    Ok(output.status)
}

fn mutate_byte_array(data: &mut [u8], lengh: usize){
    for _ in 0..10{
        data[rand::thread_rng().gen_range(0..lengh)] = rand::thread_rng().gen_range(0..256) as u8;
    }
}


//sigle thread routine for fuzzing
fn fuzz_routine(thr_id: usize, fuzzing_amount: sync::Arc<sync::Mutex<usize>>, craches_amount: sync::Arc<sync::Mutex<usize>>, corpus: sync::Arc<Vec<Vec<u8>>>, crashes_path: sync::Arc<String>, target_and_arguments: sync::Arc<Vec<String>>) -> Result<(), io::Error>{
    let thread_file_name = format!("threadFile_{}", thr_id);
    let thread_file_path = Path::new(&thread_file_name);

    let mut file_content: Vec<u8> = Vec::new();
    loop{
        //do BATCH_SIZE iterations of fuzzing
        for _ in 0..BATCH_SIZE{
            let random_file_index = rand::thread_rng().gen_range(0..corpus.len());
            
            file_content.clear();
            file_content.extend_from_slice(&corpus[random_file_index]);
            
            //mutate
            let file_len = file_content.len();
            mutate_byte_array(&mut file_content, file_len);

            //fuzz
            let exit_status = fuzz(&thread_file_path, &file_content, &target_and_arguments)?;
            if Some(11) == exit_status.signal(){
                //segmentation fault
                println!("Crash!!!");
                let mut craches = craches_amount.lock().unwrap();
                *craches += 1;
                fs::write(format!("{}/{}", crashes_path, *craches), &file_content)?;
            }
        }

        //compute statistics
        let mut amount = fuzzing_amount.lock().unwrap();
        *amount += BATCH_SIZE;
    }
}

//arg1 - threads number
//arg2 - path to dir of smaples for mutation
//arg3 - path to dir for crashes saving
//arg4 - target and argumetns
fn main() -> Result<(), io::Error> {
    let command_line_arguments:Vec<String> = env::args().collect();
    let thread_num:usize = command_line_arguments[1].parse().unwrap();
    let smaples_path = &command_line_arguments[2];
    let crashes_path = sync::Arc::new(command_line_arguments[3].clone());
    let mut target_and_arguments = Vec::new();
    target_and_arguments.extend_from_slice(&command_line_arguments[4..]);
    let target_and_arguments: sync::Arc<Vec<String>> = sync::Arc::new(target_and_arguments);

    //create directory for craches
    fs::create_dir_all(crashes_path.as_ref())?;

    //initilzation statistics
    let craches_amount = sync::Arc::new(sync::Mutex::new(0));
    let fuzzing_amount = sync::Arc::new(sync::Mutex::new(0));

    //read all files from directory to corpus
    let mut corpus_temp_collection = BTreeSet::new();
    for file_name in fs::read_dir(Path::new(smaples_path))?{
        let file_name = file_name?.path();
        corpus_temp_collection.insert(fs::read(file_name)?);
    }
    let corpus:sync::Arc<Vec<Vec<u8>>> = sync::Arc::new(corpus_temp_collection.into_iter().collect());
    println!("fuzzing with {} samples", corpus.len());


    let start = time::Instant::now();
    for thr_id in 0..thread_num{

        //threads initilzation
        let fuzzing_amount = sync::Arc::clone(&fuzzing_amount);
        let corpus = sync::Arc::clone(&corpus);
        let craches_amount = sync::Arc::clone(&craches_amount);
        let crashes_path = sync::Arc::clone(&crashes_path);
        let target_and_arguments = sync::Arc::clone(&target_and_arguments);
        thread::spawn(move || fuzz_routine(thr_id, fuzzing_amount, craches_amount, corpus, crashes_path, target_and_arguments));
    }

    loop {
        //print statitics
        thread::sleep(time::Duration::from_millis(500));
        let amount = fuzzing_amount.lock().unwrap();
        let craches = craches_amount.lock().unwrap();        
        println!("amount of fuzzing = {}, fuzzings per second = {}, craches amount = {}", *amount, *amount as f64 / start.elapsed().as_secs_f64(), *craches);
    }
}



