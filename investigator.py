#!/usr/bin/env python3
"""
INVESTIGATOR-DESK: An Investigation App That Targets the Source of Authority

This application helps investigators track and analyze sources of authority,
gather evidence, and build comprehensive investigation cases.
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional


class AuthoritySource:
    """Represents a source of authority being investigated."""
    
    def __init__(self, source_id: str, name: str, description: str, 
                 authority_type: str):
        self.source_id = source_id
        self.name = name
        self.description = description
        self.authority_type = authority_type
        self.created_at = datetime.now().isoformat()
        self.evidence: List[Dict] = []
        self.connections: List[str] = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'source_id': self.source_id,
            'name': self.name,
            'description': self.description,
            'authority_type': self.authority_type,
            'created_at': self.created_at,
            'evidence': self.evidence,
            'connections': self.connections
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AuthoritySource':
        """Create from dictionary."""
        source = cls(
            data['source_id'],
            data['name'],
            data['description'],
            data['authority_type']
        )
        source.created_at = data.get('created_at', source.created_at)
        source.evidence = data.get('evidence', [])
        source.connections = data.get('connections', [])
        return source


class Investigation:
    """Manages an investigation targeting sources of authority."""
    
    def __init__(self, investigation_id: str, title: str, description: str):
        self.investigation_id = investigation_id
        self.title = title
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.status = "active"
        self.sources: Dict[str, AuthoritySource] = {}
        self.notes: List[Dict] = []
    
    def add_authority_source(self, source: AuthoritySource):
        """Add a source of authority to this investigation."""
        self.sources[source.source_id] = source
    
    def add_evidence(self, source_id: str, evidence_type: str, 
                     description: str, source_ref: str = ""):
        """Add evidence to a specific authority source."""
        if source_id not in self.sources:
            raise ValueError(f"Authority source {source_id} not found")
        
        evidence = {
            'type': evidence_type,
            'description': description,
            'source': source_ref,
            'timestamp': datetime.now().isoformat()
        }
        self.sources[source_id].evidence.append(evidence)
    
    def add_connection(self, source_id1: str, source_id2: str):
        """Add a connection between two authority sources."""
        if source_id1 not in self.sources or source_id2 not in self.sources:
            raise ValueError("Both source IDs must exist")
        
        if source_id2 not in self.sources[source_id1].connections:
            self.sources[source_id1].connections.append(source_id2)
        if source_id1 not in self.sources[source_id2].connections:
            self.sources[source_id2].connections.append(source_id1)
    
    def add_note(self, note: str):
        """Add an investigation note."""
        self.notes.append({
            'timestamp': datetime.now().isoformat(),
            'note': note
        })
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'investigation_id': self.investigation_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'status': self.status,
            'sources': {sid: src.to_dict() for sid, src in self.sources.items()},
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Investigation':
        """Create from dictionary."""
        inv = cls(
            data['investigation_id'],
            data['title'],
            data['description']
        )
        inv.created_at = data.get('created_at', inv.created_at)
        inv.status = data.get('status', 'active')
        inv.notes = data.get('notes', [])
        
        sources_data = data.get('sources', {})
        for source_id, source_data in sources_data.items():
            inv.sources[source_id] = AuthoritySource.from_dict(source_data)
        
        return inv


class InvestigatorDesk:
    """Main application for managing investigations."""
    
    def __init__(self, data_dir: str = ".investigator-data"):
        self.data_dir = data_dir
        self.investigations: Dict[str, Investigation] = {}
        self._ensure_data_dir()
        self._load_investigations()
    
    def _ensure_data_dir(self):
        """Ensure the data directory exists."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _get_investigation_file(self, investigation_id: str) -> str:
        """Get the file path for an investigation."""
        return os.path.join(self.data_dir, f"{investigation_id}.json")
    
    def _load_investigations(self):
        """Load all investigations from disk."""
        if not os.path.exists(self.data_dir):
            return
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        inv = Investigation.from_dict(data)
                        self.investigations[inv.investigation_id] = inv
                except Exception as e:
                    print(f"Error loading {filename}: {e}", file=sys.stderr)
    
    def save_investigation(self, investigation: Investigation):
        """Save an investigation to disk."""
        filepath = self._get_investigation_file(investigation.investigation_id)
        with open(filepath, 'w') as f:
            json.dump(investigation.to_dict(), f, indent=2)
    
    def create_investigation(self, investigation_id: str, title: str, 
                           description: str) -> Investigation:
        """Create a new investigation."""
        if investigation_id in self.investigations:
            raise ValueError(f"Investigation {investigation_id} already exists")
        
        inv = Investigation(investigation_id, title, description)
        self.investigations[investigation_id] = inv
        self.save_investigation(inv)
        return inv
    
    def get_investigation(self, investigation_id: str) -> Optional[Investigation]:
        """Get an investigation by ID."""
        return self.investigations.get(investigation_id)
    
    def list_investigations(self) -> List[Investigation]:
        """List all investigations."""
        return list(self.investigations.values())
    
    def generate_report(self, investigation_id: str) -> str:
        """Generate a report for an investigation."""
        inv = self.get_investigation(investigation_id)
        if not inv:
            return f"Investigation {investigation_id} not found"
        
        report = []
        report.append("=" * 70)
        report.append(f"INVESTIGATION REPORT: {inv.title}")
        report.append("=" * 70)
        report.append(f"ID: {inv.investigation_id}")
        report.append(f"Status: {inv.status.upper()}")
        report.append(f"Created: {inv.created_at}")
        report.append(f"\nDescription: {inv.description}")
        report.append("\n" + "-" * 70)
        report.append(f"AUTHORITY SOURCES ({len(inv.sources)})")
        report.append("-" * 70)
        
        for source in inv.sources.values():
            report.append(f"\n[{source.source_id}] {source.name}")
            report.append(f"  Type: {source.authority_type}")
            report.append(f"  Description: {source.description}")
            
            if source.evidence:
                report.append(f"  Evidence ({len(source.evidence)}):")
                for i, ev in enumerate(source.evidence, 1):
                    report.append(f"    {i}. [{ev['type']}] {ev['description']}")
                    if ev.get('source'):
                        report.append(f"       Source: {ev['source']}")
            
            if source.connections:
                report.append(f"  Connections: {', '.join(source.connections)}")
        
        if inv.notes:
            report.append("\n" + "-" * 70)
            report.append(f"INVESTIGATION NOTES ({len(inv.notes)})")
            report.append("-" * 70)
            for note in inv.notes:
                report.append(f"\n[{note['timestamp']}]")
                report.append(f"  {note['note']}")
        
        report.append("\n" + "=" * 70)
        return "\n".join(report)


def main():
    """Main CLI interface."""
    print("=" * 70)
    print("INVESTIGATOR-DESK: Investigation App Targeting Source of Authority")
    print("=" * 70)
    print()
    
    desk = InvestigatorDesk()
    
    # Create a sample investigation to demonstrate functionality
    print("Creating sample investigation...")
    
    try:
        inv = desk.create_investigation(
            "INV-001",
            "Corporate Authority Structure Investigation",
            "Investigating the hierarchical authority structure and decision-making power"
        )
        
        # Add authority sources
        ceo = AuthoritySource(
            "AUTH-CEO",
            "Chief Executive Officer",
            "Primary executive authority in the organization",
            "Executive"
        )
        inv.add_authority_source(ceo)
        
        board = AuthoritySource(
            "AUTH-BOARD",
            "Board of Directors",
            "Governing body with ultimate authority over corporate decisions",
            "Governance"
        )
        inv.add_authority_source(board)
        
        cfo = AuthoritySource(
            "AUTH-CFO",
            "Chief Financial Officer",
            "Authority over financial decisions and reporting",
            "Executive"
        )
        inv.add_authority_source(cfo)
        
        # Add evidence
        inv.add_evidence(
            "AUTH-CEO",
            "Corporate Charter",
            "CEO appointed by Board of Directors with executive powers",
            "Company Charter Section 3.2"
        )
        
        inv.add_evidence(
            "AUTH-BOARD",
            "Legal Document",
            "Board has fiduciary duty and oversight authority",
            "Corporate Bylaws Article IV"
        )
        
        inv.add_evidence(
            "AUTH-CFO",
            "Financial Policy",
            "CFO reports to CEO with authority over financial operations",
            "Financial Policy Manual v2.1"
        )
        
        # Add connections
        inv.add_connection("AUTH-BOARD", "AUTH-CEO")
        inv.add_connection("AUTH-CEO", "AUTH-CFO")
        
        # Add investigation notes
        inv.add_note("Initial authority mapping completed. Clear hierarchical structure identified.")
        inv.add_note("Board of Directors identified as ultimate source of authority.")
        inv.add_note("Further investigation needed into board appointment process.")
        
        desk.save_investigation(inv)
        
        print("✓ Investigation created successfully")
        print(f"✓ Added {len(inv.sources)} authority sources")
        print(f"✓ Documented evidence and connections")
        print()
        
        # Generate and display report
        report = desk.generate_report("INV-001")
        print(report)
        
        print()
        print("Investigation data saved to:", desk.data_dir)
        print()
        print("The INVESTIGATOR-DESK app is ready for tracking authority sources!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
