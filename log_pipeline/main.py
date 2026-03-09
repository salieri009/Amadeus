import os
from adapters.file_io import LocalFileReader, LocalFileWriter
from pipeline import LogPipeline
from generator import generate_logs

def main():
    input_dir = "input_logs"
    processed_dir = "processed_logs"
    quarantine_dir = "quarantine_logs"
    
    input_file = os.path.join(input_dir, "server_logs.jsonl")
    
    if not os.path.exists(input_file):
        print("Fake data not found. Generating logs...")
        generate_logs(num_logs=200, output_dir=input_dir)
        
    print("Setting up I/O Adapters...")
    reader = LocalFileReader(file_path=input_file)
    processed_writer = LocalFileWriter(directory=processed_dir)
    quarantine_writer = LocalFileWriter(directory=quarantine_dir)
    
    pipeline = LogPipeline(
        reader=reader,
        processed_writer=processed_writer,
        quarantine_writer=quarantine_writer
    )
    
    print("Running Log Validation Pipeline...")
    pipeline.run()
    
if __name__ == "__main__":
    main()
