#!/usr/bin/env python3
import re
import quopri

def extract_and_decode_html(mhtml_file):
    """Extract HTML content from MHTML file and decode it."""
    with open(mhtml_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find the HTML section
    html_start = content.find('<!DOCTYPE html>')
    if html_start == -1:
        html_start = content.find('<html')
    
    if html_start == -1:
        return None
    
    html_content = content[html_start:]
    
    # Decode quoted-printable if present
    try:
        decoded_html = quopri.decodestring(html_content.encode('utf-8')).decode('utf-8')
        return decoded_html
    except:
        return html_content

def debug_option_extraction(mhtml_file):
    """Debug the option extraction process."""
    print(f"Debugging option extraction from: {mhtml_file}")
    
    # Extract HTML
    html_content = extract_and_decode_html(mhtml_file)
    if not html_content:
        print("❌ Failed to extract HTML")
        return
    
    print(f"✅ Successfully extracted HTML ({len(html_content)} characters)")
    
    # Find question blocks
    question_pattern = r'<div[^>]*class="[^"]*Qr7Oae[^"]*"[^>]*role="listitem"[^>]*>.*?</div>(?=\s*<div[^>]*class="[^"]*Qr7Oae[^"]*"[^>]*role="listitem"|\s*</div>\s*</div>\s*$)'
    question_blocks = re.findall(question_pattern, html_content, re.DOTALL)
    
    print(f"\n📊 Question blocks found: {len(question_blocks)}")
    
    # Test first few question blocks
    for i, question_block in enumerate(question_blocks[:3]):
        print(f"\n--- Question {i+1} ---")
        
        # Extract all options using the same pattern as quiz_toolkit.py
        option_pattern = r'<span[^>]*class="[^"]*aDTYNe[^"]*"[^>]*>([^<]+)</span>'
        all_options = re.findall(option_pattern, question_block)
        
        print(f"Raw options found: {len(all_options)}")
        for j, option in enumerate(all_options):
            print(f"  Raw {j+1}: '{option}'")
        
        # Apply the same filtering logic as quiz_toolkit.py
        options = []
        for option in all_options:
            clean_option = re.sub(r'\s+', ' ', option.strip())
            clean_option = re.sub(r'^[\\"]+|[\\"]+$', '', clean_option)
            clean_option = re.sub(r'^\s+|\s+$', '', clean_option)
            
            print(f"  Cleaned: '{clean_option}'")
            
            # Test both regex patterns
            pattern1_match = re.match(r'^(\([A-Da-d1-9]\)|[A-Da-d1-9][\.\.\)\]])', clean_option)
            pattern2_match = re.match(r'^[1-9]\. ', clean_option)
            
            print(f"    Pattern 1 (letters/numbers): {bool(pattern1_match)}")
            print(f"    Pattern 2 (number + period + space): {bool(pattern2_match)}")
            
            if clean_option and (pattern1_match or pattern2_match) and clean_option not in options:
                options.append(clean_option)
                print(f"    ✅ ACCEPTED")
            else:
                print(f"    ❌ REJECTED")
        
        print(f"Final filtered options: {len(options)}")
        for j, option in enumerate(options):
            print(f"  {j+1}. {option}")

if __name__ == "__main__":
    mhtml_file = "/Users/rjmolina13/Documents/Code_Stuff/mockexam_gform/Sir Ikel _ Science Majorship Intensive Series – Physics (Session 3).mhtml"
    debug_option_extraction(mhtml_file)