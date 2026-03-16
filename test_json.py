import json, re

def extract_json_from_response(text):
    if not text: return None
    json_patterns = [r'```json\s*([\s\S]*?)\s*```', r'```\s*([\s\S]*?)\s*```', r'\{[\s\S]*"edits"[\s\S]*\}']
    
    for pattern in json_patterns:
        match = re.search(pattern, text)
        if match:
            print('Matched pattern:', pattern[:15], '...')
            try:
                json_str = match.group(1) if '```' in pattern else match.group(0)
                return json.loads(json_str)
            except Exception as e:
                print('JSON parse error:', e)
                # Print the line that failed
                lines = json_str.split('\n')
                # Try to find exactly where it failed from error message (e.g. "Expecting ',' delimiter: line 42")
                try:
                    err_str = str(e)
                    line_num = int(re.search(r'line (\d+)', err_str).group(1))
                    print(f"Error around line {line_num}:")
                    print(lines[line_num-2])
                    print(lines[line_num-1], "   <--- ERROR HERE")
                    print(lines[line_num])
                except:
                    pass
                continue
    return None

with open('api/ai_communication.md', 'r', encoding='utf-8') as f:
    log_content = f.read()

# Find ALL Executor JSON blocks
blocks = re.findall(r'\*\*Executor\*\*: ```json\n(.*?)\n```', log_content, re.DOTALL)
if blocks:
    for index, block in enumerate(blocks):
        current_block = '```json\n{' + block.split('{', 1)[-1] if '{' in block else block + '\n```'
        print(f"Testing parser on block {index + 1}/{len(blocks)} (length: {len(current_block)})...")
        result = extract_json_from_response(current_block)
        if result:
            print("Success! Keys:", result.keys())
        else:
            print("Failed completely")
else:
    print("No blocks found")
