#!/usr/bin/env python3
"""
LEXIS NEXIS REPORT PARSER FOR INVESTIGATOR-DESK

Parses Lexis Nexis reports (PDF, JSON, TXT, CSV) and imports data into InvestigatorDesk.
Supports background checks, public records, court records, addresses, and associates.

Usage:
    from lexis_nexis_parser import LexisNexisParser
    from investigator import InvestigatorDesk
    
    parser = LexisNexisParser()
    desk = InvestigatorDesk()
    inv = desk.create_investigation("INV-003", "Background Check", "Subject investigation")
    
    # Parse and import Lexis Nexis data
    parser.parse_and_import(inv, "lexis_report.pdf")  # or .json, .txt, .csv
    desk.save_investigation(inv)
"""

import json
import re
import csv
import sys
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

# Import from investigator.py
try:
    from investigator import AuthoritySource, Investigation
except ImportError:
    print("Warning: investigator.py not found.", file=sys.stderr)
    AuthoritySource = None
    Investigation = None


class LexisNexisParser:
    """
    Multi-format parser for Lexis Nexis reports.
    Handles PDF, JSON, plain text, and CSV formats.
    """
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.json', '.txt', '.csv', '.html']
        
    def parse_and_import(self, investigation: 'Investigation', file_path: str, 
                        subject_name: Optional[str] = None) -> int:
        """
        Parse a Lexis Nexis report and import into investigation.
        
        Args:
            investigation: Investigation object to import into
            file_path: Path to Lexis Nexis report file
            subject_name: Name of subject (extracted from filename if not provided)
        
        Returns:
            Number of authority sources added
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Report file not found: {file_path}")
        
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported format: {file_ext}. Supported: {self.supported_formats}")
        
        # Extract subject name from filename if not provided
        if not subject_name:
            subject_name = Path(file_path).stem.replace('_', ' ').replace('-', ' ')
        
        print(f"Parsing Lexis Nexis report: {file_path}")
        print(f"Subject: {subject_name}")
        
        # Route to appropriate parser
        if file_ext == '.json':
            data = self._parse_json(file_path)
        elif file_ext == '.csv':
            data = self._parse_csv(file_path)
        elif file_ext == '.txt':
            data = self._parse_text(file_path)
        elif file_ext == '.pdf':
            data = self._parse_pdf(file_path)
        elif file_ext == '.html':
            data = self._parse_html(file_path)
        else:
            data = {}
        
        # Import parsed data into investigation
        added_count = self._import_to_investigation(investigation, data, subject_name, file_path)
        
        return added_count
    
    def _parse_json(self, file_path: str) -> Dict:
        """
        Parse JSON format Lexis Nexis report.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Normalize structure
        parsed = {
            'subject': data.get('subject', {}),
            'addresses': data.get('addresses', []),
            'phones': data.get('phones', data.get('phone_numbers', [])),
            'associates': data.get('associates', data.get('relatives', [])),
            'court_records': data.get('court_records', data.get('legal_records', [])),
            'liens_judgments': data.get('liens', data.get('judgments', [])),
            'businesses': data.get('businesses', data.get('business_affiliations', [])),
            'properties': data.get('properties', data.get('real_estate', [])),
            'raw_data': data
        }
        
        return parsed
    
    def _parse_csv(self, file_path: str) -> Dict:
        """
        Parse CSV format Lexis Nexis export.
        """
        parsed = {
            'addresses': [],
            'phones': [],
            'associates': [],
            'court_records': [],
            'raw_data': []
        }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                parsed['raw_data'].append(row)
                
                # Categorize based on common column patterns
                if 'address' in ' '.join(row.keys()).lower():
                    parsed['addresses'].append(row)
                if 'phone' in ' '.join(row.keys()).lower():
                    parsed['phones'].append(row)
                if 'associate' in ' '.join(row.keys()).lower() or 'relative' in ' '.join(row.keys()).lower():
                    parsed['associates'].append(row)
                if 'court' in ' '.join(row.keys()).lower() or 'case' in ' '.join(row.keys()).lower():
                    parsed['court_records'].append(row)
        
        return parsed
    
    def _parse_text(self, file_path: str) -> Dict:
        """
        Parse plain text Lexis Nexis report using regex patterns.
        """
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        parsed = {
            'addresses': self._extract_addresses(text),
            'phones': self._extract_phones(text),
            'associates': self._extract_associates(text),
            'court_records': self._extract_court_records(text),
            'liens_judgments': self._extract_liens_judgments(text),
            'raw_text': text
        }
        
        return parsed
    
    def _parse_pdf(self, file_path: str) -> Dict:
        """
        Parse PDF Lexis Nexis report.
        Requires PyPDF2 or pdfplumber. Falls back to text extraction.
        """
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except ImportError:
            try:
                import pdfplumber
                text = ""
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
            except ImportError:
                print("Warning: PDF parsing requires PyPDF2 or pdfplumber. Install with: pip install PyPDF2", file=sys.stderr)
                return {'raw_text': '[PDF parsing library not available]'}
        
        # Parse extracted text
        return self._parse_text_content(text)
    
    def _parse_html(self, file_path: str) -> Dict:
        """
        Parse HTML format Lexis Nexis report.
        """
        try:
            from bs4 import BeautifulSoup
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            text = soup.get_text()
            return self._parse_text_content(text)
        except ImportError:
            print("Warning: HTML parsing requires beautifulsoup4. Install with: pip install beautifulsoup4", file=sys.stderr)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return {'raw_text': text}
    
    def _parse_text_content(self, text: str) -> Dict:
        """
        Parse extracted text content from any source.
        """
        return {
            'addresses': self._extract_addresses(text),
            'phones': self._extract_phones(text),
            'associates': self._extract_associates(text),
            'court_records': self._extract_court_records(text),
            'liens_judgments': self._extract_liens_judgments(text),
            'raw_text': text
        }
    
    def _extract_addresses(self, text: str) -> List[Dict]:
        """
        Extract addresses using regex patterns.
        """
        addresses = []
        
        # Pattern: Street address with city, state, zip
        pattern = r'(\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd|Court|Ct|Way|Place|Pl)[\w\s,]*[A-Z]{2}\s+\d{5}(?:-\d{4})?)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        for match in matches:
            addresses.append({
                'address': match.strip(),
                'source': 'Extracted from report'
            })
        
        return addresses
    
    def _extract_phones(self, text: str) -> List[Dict]:
        """
        Extract phone numbers using regex.
        """
        phones = []
        
        # Various phone patterns
        patterns = [
            r'\(?\d{3}\)?[-\s.]?\d{3}[-\s.]?\d{4}',  # (123) 456-7890 or 123-456-7890
            r'\d{3}[-\s.]\d{3}[-\s.]\d{4}',  # 123.456.7890
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                phones.append({
                    'number': match.strip(),
                    'type': 'Unknown'
                })
        
        return phones
    
    def _extract_associates(self, text: str) -> List[Dict]:
        """
        Extract associate/relative names.
        """
        associates = []
        
        # Look for sections with associate/relative keywords
        sections = re.split(r'(?:Associates?|Relatives?|Known Associates|Possible Relatives):', text, flags=re.IGNORECASE)
        
        if len(sections) > 1:
            # Extract names from associate sections
            for section in sections[1:]:
                # Simple name pattern: Capitalized words
                names = re.findall(r'\b([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', section[:500])  # First 500 chars
                for name in names:
                    associates.append({
                        'name': name,
                        'relationship': 'Associate/Relative'
                    })
        
        return associates
    
    def _extract_court_records(self, text: str) -> List[Dict]:
        """
        Extract court records and case information.
        """
        records = []
        
        # Look for case numbers
        case_pattern = r'Case\s*(?:Number|No\.?|#)?\s*:?\s*([\w-]+)'
        cases = re.findall(case_pattern, text, re.IGNORECASE)
        
        for case in cases:
            records.append({
                'case_number': case,
                'type': 'Court Record',
                'source': 'Lexis Nexis Report'
            })
        
        return records
    
    def _extract_liens_judgments(self, text: str) -> List[Dict]:
        """
        Extract liens and judgments.
        """
        liens = []
        
        # Look for lien/judgment keywords
        if re.search(r'\b(lien|judgment|levy)\b', text, re.IGNORECASE):
            liens.append({
                'type': 'Financial Record',
                'description': 'Lien or judgment found in report',
                'source': 'Lexis Nexis Report'
            })
        
        return liens
    
    def _import_to_investigation(self, investigation: 'Investigation', data: Dict, 
                                 subject_name: str, source_file: str) -> int:
        """
        Import parsed data into Investigation as AuthoritySource objects.
        """
        if AuthoritySource is None or Investigation is None:
            raise ImportError("investigator.py classes not available")
        
        added_count = 0
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Add subject profile
        subject_source = AuthoritySource(
            source_id=f"LEXIS-SUBJECT-{timestamp}",
            name=f"{subject_name} - Background Profile",
            description=f"Lexis Nexis background check profile from {source_file}",
            authority_type="Background Check"
        )
        subject_source.evidence.append({
            'type': 'Background Report',
            'description': f"Complete Lexis Nexis report for {subject_name}",
            'source': f"Lexis Nexis Report: {source_file}",
            'timestamp': datetime.now().isoformat()
        })
        investigation.add_authority_source(subject_source)
        added_count += 1
        
        # Add addresses
        if data.get('addresses'):
            addr_source = AuthoritySource(
                source_id=f"LEXIS-ADDR-{timestamp}",
                name=f"{subject_name} - Address History",
                description=f"Known addresses from Lexis Nexis ({len(data['addresses'])} found)",
                authority_type="Address Records"
            )
            for i, addr in enumerate(data['addresses'][:10], 1):  # Limit to 10
                addr_str = addr if isinstance(addr, str) else addr.get('address', str(addr))
                addr_source.evidence.append({
                    'type': 'Address',
                    'description': f"Address #{i}: {addr_str}",
                    'source': 'Lexis Nexis',
                    'timestamp': datetime.now().isoformat()
                })
            investigation.add_authority_source(addr_source)
            added_count += 1
        
        # Add phone numbers
        if data.get('phones'):
            phone_source = AuthoritySource(
                source_id=f"LEXIS-PHONE-{timestamp}",
                name=f"{subject_name} - Phone Numbers",
                description=f"Known phone numbers from Lexis Nexis ({len(data['phones'])} found)",
                authority_type="Contact Records"
            )
            for i, phone in enumerate(data['phones'][:10], 1):
                phone_str = phone if isinstance(phone, str) else phone.get('number', str(phone))
                phone_source.evidence.append({
                    'type': 'Phone Number',
                    'description': f"Phone #{i}: {phone_str}",
                    'source': 'Lexis Nexis',
                    'timestamp': datetime.now().isoformat()
                })
            investigation.add_authority_source(phone_source)
            added_count += 1
        
        # Add associates/relatives
        if data.get('associates'):
            assoc_source = AuthoritySource(
                source_id=f"LEXIS-ASSOC-{timestamp}",
                name=f"{subject_name} - Associates & Relatives",
                description=f"Known associates from Lexis Nexis ({len(data['associates'])} found)",
                authority_type="Associate Network"
            )
            for i, assoc in enumerate(data['associates'][:10], 1):
                assoc_str = assoc if isinstance(assoc, str) else assoc.get('name', str(assoc))
                assoc_source.evidence.append({
                    'type': 'Associate',
                    'description': f"Associate #{i}: {assoc_str}",
                    'source': 'Lexis Nexis',
                    'timestamp': datetime.now().isoformat()
                })
            investigation.add_authority_source(assoc_source)
            added_count += 1
        
        # Add court records
        if data.get('court_records'):
            court_source = AuthoritySource(
                source_id=f"LEXIS-COURT-{timestamp}",
                name=f"{subject_name} - Court Records",
                description=f"Court records from Lexis Nexis ({len(data['court_records'])} found)",
                authority_type="Legal Records"
            )
            for i, record in enumerate(data['court_records'][:10], 1):
                record_str = record if isinstance(record, str) else record.get('case_number', str(record))
                court_source.evidence.append({
                    'type': 'Court Record',
                    'description': f"Record #{i}: {record_str}",
                    'source': 'Lexis Nexis',
                    'timestamp': datetime.now().isoformat()
                })
            investigation.add_authority_source(court_source)
            added_count += 1
        
        # Add liens/judgments
        if data.get('liens_judgments'):
            lien_source = AuthoritySource(
                source_id=f"LEXIS-LIEN-{timestamp}",
                name=f"{subject_name} - Liens & Judgments",
                description=f"Financial records from Lexis Nexis ({len(data['liens_judgments'])} found)",
                authority_type="Financial Records"
            )
            for i, lien in enumerate(data['liens_judgments'][:10], 1):
                lien_str = lien if isinstance(lien, str) else lien.get('description', str(lien))
                lien_source.evidence.append({
                    'type': 'Lien/Judgment',
                    'description': f"Record #{i}: {lien_str}",
                    'source': 'Lexis Nexis',
                    'timestamp': datetime.now().isoformat()
                })
            investigation.add_authority_source(lien_source)
            added_count += 1
        
        # Add investigation note
        investigation.add_note(
            f"Imported Lexis Nexis report: {source_file} | Subject: {subject_name} | "
            f"{added_count} authority sources added | Parser: LexisNexisParser v1.0"
        )
        
        return added_count


def demo():
    """
    Demonstration of LexisNexisParser.
    """
    print("="*70)
    print("LEXIS NEXIS REPORT PARSER - DEMONSTRATION")
    print("="*70)
    print()
    
    parser = LexisNexisParser()
    
    print("Supported formats:")
    for fmt in parser.supported_formats:
        print(f"  - {fmt}")
    print()
    
    # Demo text parsing
    sample_text = """Subject: John Doe
    
Addresses:
123 Main Street, Phoenix, AZ 85001
456 Oak Avenue, Tucson, AZ 85701

Phone Numbers:
(602) 555-1234
520-555-5678

Known Associates:
Jane Doe
Michael Smith

Court Records:
Case Number: CV2023-001234
Case Number: CR2022-005678
    """
    
    print("Parsing sample text...")
    data = parser._parse_text_content(sample_text)
    
    print(f"\nExtracted data:")
    print(f"  Addresses: {len(data['addresses'])}")
    print(f"  Phones: {len(data['phones'])}")
    print(f"  Associates: {len(data['associates'])}")
    print(f"  Court Records: {len(data['court_records'])}")
    print()
    
    # Integration test
    if Investigation and AuthoritySource:
        print("-"*70)
        print("Testing integration with InvestigatorDesk...")
        
        try:
            from investigator import InvestigatorDesk
            
            desk = InvestigatorDesk()
            inv = desk.create_investigation(
                "LEXIS-DEMO-001",
                "Background Check Demo",
                "Demonstration of Lexis Nexis report import"
            )
            
            # Simulate importing parsed data
            added = parser._import_to_investigation(inv, data, "John Doe", "sample_report.txt")
            desk.save_investigation(inv)
            
            print(f"✓ Created investigation: {inv.investigation_id}")
            print(f"✓ Added {added} authority sources from Lexis Nexis report")
            print(f"✓ Saved to: {desk.data_dir}")
            
        except Exception as e:
            print(f"Integration test failed: {e}")
    else:
        print("Skipping integration test (investigator.py not found)")
    
    print("\n" + "="*70)
    print("Demo complete!")
    print("\nUsage: parser.parse_and_import(investigation, 'your_lexis_report.pdf')")
    print("="*70)


if __name__ == "__main__":
    demo()
