import os

def is_text_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read(2048)
        return True
    except:
        return False

def save_structure(root_folder, structure_file):
    with open(structure_file, 'w', encoding='utf-8') as out:
        for dirpath, dirnames, filenames in os.walk(root_folder):
            level = dirpath.replace(root_folder, '').count(os.sep)
            indent = '│   ' * level
            folder_name = os.path.basename(dirpath)
            out.write(f"{indent}📁 {folder_name}\n")
            sub_indent = '│   ' * (level + 1)
            for filename in filenames:
                out.write(f"{sub_indent}📄 {filename}\n")

def save_file_contents(root_folder, contents_file, max_size_mb=5):
    with open(contents_file, 'w', encoding='utf-8') as out:
        for dirpath, _, filenames in os.walk(root_folder):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, root_folder)
                try:
                    size_mb = os.path.getsize(full_path) / (1024 * 1024)
                    if size_mb > max_size_mb:
                        out.write(f"\n[Skipping large file > {max_size_mb}MB: {relative_path}]\n")
                        continue

                    if not is_text_file(full_path):
                        out.write(f"\n[Skipping binary or unreadable file: {relative_path}]\n")
                        continue

                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    out.write(f"\n{'='*100}\n")
                    out.write(f"📄 File: {filename}\n📂 Path: {relative_path}\n")
                    out.write(f"{'-'*100}\n{content}\n")
                    out.write(f"{'='*100}\n")

                except Exception as e:
                    out.write(f"\n[Error reading file: {relative_path} | {e}]\n")

def main():
    folder = r"D:\HindiTTS\tacotronGrok\tacotron"
    structure_output = "structure.txt"
    contents_output = "file_contents.txt"

    if not os.path.isdir(folder):
        print("❌ Invalid folder path.")
        return

    save_structure(folder, structure_output)
    save_file_contents(folder, contents_output)

    print(f"\n✅ Folder structure saved to: {structure_output}")
    print(f"✅ File contents saved to: {contents_output}")

if __name__ == "__main__":
    main()
