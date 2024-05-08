#!/usr/bin/env python

import os
from qiskit_serverless import ServerlessProvider, QiskitFunction

serverless = ServerlessProvider(
    token=os.environ.get("GATEWAY_TOKEN", "awesome_token"),
    host=os.environ.get("GATEWAY_HOST", "http://localhost:8000"),
)
print(serverless)

function = QiskitFunction(
    title="file-producer", entrypoint="produce_files.py", working_dir="./source_files/"
)
serverless.upload(function)

job = serverless.run("file-producer")
print(job)

print(job.result())
print(job.status())
print(job.logs())

available_files = serverless.files()
print(available_files)

if len(available_files) > 0:
    serverless.file_download(available_files[0])
print("Download complete")
