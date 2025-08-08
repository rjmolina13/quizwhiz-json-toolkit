#!/usr/bin/env python3
"""
Debug script for Physics Session 3 MHTML extraction
"""

import re
import quopri

def extract_html_from_mhtml(mhtml_file):
    """Extract HTML content from MHTML file"""
    try:
        with open(mhtml_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Find the HTML section
        html_start = content.find('Content-Type: text/html')
        if html_start == -1:
            return None
        
        # Find the actual HTML content (after headers)
        html_content_start = content.find('\n\n', html_start)
        if html_content_start == -1:
            return None
        
        # Find the end boundary
        boundary_start = content.find('------MultipartBoundary', html_content_start + 2)
        if boundary_start == -1:
            html_content = content[html_content_start + 2:]
        else:
            html_content = content[html_content_start + 2:boundary_start]
        
        # Decode quoted-printable
        try:
            decoded_html = quopri.decodestring(html_content.encode('utf-8')).decode('utf-8', errors='ignore')
            return decoded_html
        except Exception as e:
            print(f"Error decoding quoted-printable: {e}")
            return html_content
    
    except Exception as e:
        print(f"Error reading MHTML file: {e}")
        return None

def debug_extraction(mhtml_file):
    """Debug the extraction process"""
    print(f"Debugging extraction from: {mhtml_file}")
    
    # Extract HTML
    decoded_html = extract_html_from_mhtml(mhtml_file)
    if not decoded_html:
        print("❌ Failed to extract HTML from MHTML")
        return
    
    print(f"✅ Successfully extracted HTML ({len(decoded_html)} characters)")
    
    # Test question block pattern
    question_block_pattern = r'<div[^>]*class="[^"]*Qr7Oae[^"]*"[^>]*role="listitem"[^>]*>.*?(?=<div[^>]*class="[^"]*Qr7Oae[^"]*"[^>]*role="listitem"|$)'
    question_blocks = re.findall(question_block_pattern, decoded_html, re.DOTALL)
    
    print(f"\n📊 Question blocks found: {len(question_blocks)}")
    
    if len(question_blocks) == 0:
        print("\n🔍 Searching for alternative patterns...")
        
        # Check for Qr7Oae without role
        qr7oae_pattern = r'<div[^>]*class="[^"]*Qr7Oae[^"]*"[^>]*>'
        qr7oae_matches = re.findall(qr7oae_pattern, decoded_html)
        print(f"   Qr7Oae divs (any): {len(qr7oae_matches)}")
        
        # Check for role="listitem"
        listitem_pattern = r'role="listitem"'
        listitem_matches = re.findall(listitem_pattern, decoded_html)
        print(f"   role=\"listitem\" elements: {len(listitem_matches)}")
        
        # Check for M7eMe spans
        m7eme_pattern = r'<span[^>]*class="[^"]*M7eMe[^"]*"[^>]*>'
        m7eme_matches = re.findall(m7eme_pattern, decoded_html)
        print(f"   M7eMe spans: {len(m7eme_matches)}")
        
        # Show first few characters of HTML for inspection
        print(f"\n📝 First 1000 characters of decoded HTML:")
        print(decoded_html[:1000])
        print("...")
        
        return
    
    # Test question text extraction from first few blocks
    print(f"\n🔍 Testing question text extraction from first 3 blocks:")
    
    for i, question_block in enumerate(question_blocks[:3]):
        print(f"\n--- Question {i+1} ---")
        
        # Extract question text using M7eMe pattern
        question_text = None
        m7eme_start = re.search(r'<span[^>]*class="[^"]*M7eMe[^"]*"[^>]*>', question_block)
        if m7eme_start:
            start_pos = m7eme_start.end()
            content = question_block[start_pos:]
            span_count = 1
            pos = 0
            while span_count > 0 and pos < len(content):
                next_open = content.find('<span', pos)
                next_close = content.find('</span>', pos)
                
                if next_close == -1:
                    break
                if next_open != -1 and next_open < next_close:
                    span_count += 1
                    pos = next_open + 5
                else:
                    span_count -= 1
                    if span_count == 0:
                        question_text = content[:next_close]
                        break
                    pos = next_close + 7
        
        if question_text:
            # Clean the text
            clean_text = re.sub(r'<[^>]+>', '', question_text)
            clean_text = re.sub(r'\s+', ' ', clean_text.strip())
            clean_text = re.sub(r'^["\']|["\']$', '', clean_text)
            clean_text = re.sub(r'^\d+\.\s*', '', clean_text)
            
            print(f"Raw text: {question_text[:100]}...")
            print(f"Clean text: {clean_text}")
        else:
            print("❌ No M7eMe span found")
        
        # Extract options using aDTYNe pattern
        option_pattern = r'<span[^>]*class="[^"]*aDTYNe[^"]*"[^>]*>([^<]+)</span>'
        all_options = re.findall(option_pattern, question_block)
        
        print(f"Options found: {len(all_options)}")
        for j, option in enumerate(all_options[:4]):
            clean_option = re.sub(r'\s+', ' ', option.strip())
            print(f"  {j+1}. {clean_option}")

if __name__ == "__main__":
    mhtml_file = "/Users/rjmolina13/Documents/Code_Stuff/mockexam_gform/Sir Ikel _ Science Majorship Intensive Series – Physics (Session 3).mhtml"
    debug_extraction(mhtml_file)