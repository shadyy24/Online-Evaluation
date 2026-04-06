import os

def replace_color_in_file(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, not found")
        return
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin-1') as f:
            content = f.read()
            
    # Primary Blue to Violet
    content = content.replace('#007bff', '#8a2be2')
    content = content.replace('#0069d9', '#6f22b5') # darker shade for hover
    content = content.replace('#0062cc', '#6820a8') # even darker
    
    # Skydash Primary Indigo to Violet
    content = content.replace('#4B49AC', '#8a2be2')
    content = content.replace('#3f3e91', '#6f22b5')
    
    # Other accents (like teal/success) maybe to a complementary color? We'll just stick to primary for now.
    content = content.replace('rgba(0, 123, 255', 'rgba(138, 43, 226')
    content = content.replace('rgba(75, 73, 172', 'rgba(138, 43, 226')

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    except Exception as e:
        print(f"Failed to write to {filepath}: {e}")

# Target paths
base_dir = r"c:\Users\sivak\OneDrive\Documents\wsnpwap\project\assessment_tool\assessment_tool\static"

css_files = [
    os.path.join(base_dir, r"des2\css\style.css"),
    os.path.join(base_dir, r"css\vertical-layout-light\style.css"),
    os.path.join(base_dir, r"des2\css\bootstrap.min.css")
]

for filepath in css_files:
    replace_color_in_file(filepath)
