# boostnote2markdown - Convert Boostnote local storage to directory structure with Markdown files
# Copyright Martin Miedema 2021
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import json
import glob
import os
import warnings
from pathlib import Path
from shutil import copyfile

# Disable deprication warnings, not much we can do to avoid those.
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Find all .json files in the notes directory
paths = glob.glob("notes/*.json")

# Inventory attachments
attachments = glob.glob("attachments/*")

def write_file(folder, title, content):
    # Unescape the content
    content = data['content'].encode().decode('unicode-escape')

    if not os.path.isdir(path.parent):
        os.makedirs(path.parent)

    # Check if any attachments are referenced:
    for attachment in attachments:
        # Check if the attachment name is referenced with ](attachment_name)
        if f']({attachment.replace("attachments/", "")})' in content:
            # Copy the file and remove the atachment from the list.
            copyfile(f'{attachment}', f'{path.parent}/{attachment.replace("attachments/","")}')
            attachments.remove(attachment)
    # Write the content to the file
    with open(path.__str__().lstrip("/"), 'w') as output_file:
        output_file.write(content)

untitled_counter = 1
for file in paths:
    with open(file) as json_file:
        data = json.load(json_file)

    # Create the directory and file name using the title if it has one.
    if data['title'] and data['content']:
        path = Path(f"{data['folderPathname'].strip('/')}/{data['title']}.md")
        write_file(path, data['title'], data['content'])

    # If there is content, but no title, create a untitled file using the counter
    elif data['content']:
        path = Path(f"{data['folderPathname'].strip('/')}/untitled_{untitled_counter:03d}.md")
        write_file(path, data['title'], data['content'])
        untitled_counter = untitled_counter + 1

    else:
        print (f"File '{file}' has no content")

# Output any attachments that were not used:
for file in attachments:
    print (f"No note found for attachment: {file}")
