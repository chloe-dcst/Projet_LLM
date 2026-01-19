from load import load_file
import re

def chunk_file(path:str, content_file:str) -> list:
    
    content = load_file(path)
    chunks = []
    lines = content.split('\n')
    current_chunk = []
    h1_context = ""
    
    for line in lines:
        if re.match(r'^# ', line):
            if current_chunk:
                chunks.append('\n'.join(current_chunk).strip())
            h1_context = line
            current_chunk = []
        elif re.match(r'^## ', line):
            if current_chunk:
                chunks.append('\n'.join(current_chunk).strip())
            current_chunk = [h1_context, line] if h1_context else [line]
        else:
            current_chunk.append(line)
    
    if current_chunk:
        chunks.append('\n'.join(current_chunk).strip())
    
    return chunks    

chunks = chunk_file('data/projets.md', load_file('data/projets.md'))
for i, chunk in enumerate(chunks, 1):
    print(f"\n{'='*60}\nCHUNK {i}\n{'='*60}")
    print(chunk)

    
