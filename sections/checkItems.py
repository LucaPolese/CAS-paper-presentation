import os
import re

def process_itemize_block(block):
    """Process an itemize block to ensure each \item ends with the correct punctuation."""
    items = block.split(r'\item')
    processed_items = []

    for i, item in enumerate(items):
        if i == 0:
            # This is the text before the first \item, keep it as is
            processed_items.append(item)
            continue

        # Preserve the existing indentation
        lines = item.split('\n')
        indent = len(lines[0]) - len(lines[0].lstrip())
        indent_str = lines[0][:indent]

        item = item.strip()
        if i == len(items) - 1:
            # Last item should end with a period
            if not item.endswith('.'):
                item = re.sub(r'[;.]?$', '.', item)
        else:
            # Intermediate items should end with a semicolon
            if not item.endswith(';'):
                item = re.sub(r'[;.]?$', ';', item)
        
        processed_items.append(f'{indent_str}\\item {item}')

    return ''.join(processed_items)

def check_and_fix_tex_file(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Find all itemize blocks
    itemize_blocks = re.findall(r'(\\begin{itemize}.*?\\end{itemize})', content, re.DOTALL)

    for block in itemize_blocks:
        fixed_block = process_itemize_block(block)
        content = content.replace(block, fixed_block)

    with open(filename, 'w') as file:
        file.write(content)

def main():
    tex_files = [f for f in os.listdir() if f.endswith('.tex')]

    for tex_file in tex_files:
        check_and_fix_tex_file(tex_file)
        print(f'Processed file: {tex_file}')

if __name__ == "__main__":
    main()
