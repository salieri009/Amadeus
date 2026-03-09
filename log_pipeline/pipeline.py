import os
from pydantic import ValidationError
from models.log_model import ServerLog
from adapters.file_io import LocalFileReader, LocalFileWriter

class LogPipeline:
    def __init__(self, reader: LocalFileReader, processed_writer: LocalFileWriter, quarantine_writer: LocalFileWriter):
        self.reader = reader
        self.processed_writer = processed_writer
        self.quarantine_writer = quarantine_writer
        
    def run(self):
        processed_count = 0
        quarantine_count = 0
        
        for line in self.reader.read_lines():
            try:
                # Pydantic validation
                ServerLog.model_validate_json(line)
                self.processed_writer.write_line("valid_logs.jsonl", line)
                processed_count += 1
            except ValidationError as e:
                # We can inject the error reason into the quarantined log, but for now we'll just save it as is
                self.quarantine_writer.write_line("quarantined_logs.jsonl", line)
                quarantine_count += 1
                
        print(f"Pipeline finished processing logs.")
        print(f"Valid Logs: {processed_count}")
        print(f"Quarantined Logs: {quarantine_count}")
