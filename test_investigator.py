#!/usr/bin/env python3
"""
Tests for INVESTIGATOR-DESK application.
Validates core functionality of the investigation app.
"""

import os
import sys
import json
import shutil
import tempfile
from investigator import InvestigatorDesk, Investigation, AuthoritySource


def test_authority_source_creation():
    """Test creating an authority source."""
    source = AuthoritySource(
        "TEST-001",
        "Test Authority",
        "A test authority source",
        "Test Type"
    )
    
    assert source.source_id == "TEST-001"
    assert source.name == "Test Authority"
    assert source.description == "A test authority source"
    assert source.authority_type == "Test Type"
    assert len(source.evidence) == 0
    assert len(source.connections) == 0
    print("✓ Authority source creation test passed")


def test_investigation_creation():
    """Test creating an investigation."""
    inv = Investigation(
        "INV-TEST",
        "Test Investigation",
        "A test investigation"
    )
    
    assert inv.investigation_id == "INV-TEST"
    assert inv.title == "Test Investigation"
    assert inv.description == "A test investigation"
    assert inv.status == "active"
    assert len(inv.sources) == 0
    assert len(inv.notes) == 0
    print("✓ Investigation creation test passed")


def test_add_authority_source():
    """Test adding authority sources to an investigation."""
    inv = Investigation("INV-TEST", "Test", "Test investigation")
    source = AuthoritySource("AUTH-001", "Authority 1", "Test", "Type 1")
    
    inv.add_authority_source(source)
    
    assert len(inv.sources) == 1
    assert "AUTH-001" in inv.sources
    assert inv.sources["AUTH-001"].name == "Authority 1"
    print("✓ Add authority source test passed")


def test_add_evidence():
    """Test adding evidence to an authority source."""
    inv = Investigation("INV-TEST", "Test", "Test investigation")
    source = AuthoritySource("AUTH-001", "Authority 1", "Test", "Type 1")
    inv.add_authority_source(source)
    
    inv.add_evidence(
        "AUTH-001",
        "Document",
        "Test evidence",
        "Source reference"
    )
    
    assert len(inv.sources["AUTH-001"].evidence) == 1
    evidence = inv.sources["AUTH-001"].evidence[0]
    assert evidence['type'] == "Document"
    assert evidence['description'] == "Test evidence"
    assert evidence['source'] == "Source reference"
    print("✓ Add evidence test passed")


def test_add_connections():
    """Test adding connections between authority sources."""
    inv = Investigation("INV-TEST", "Test", "Test investigation")
    source1 = AuthoritySource("AUTH-001", "Authority 1", "Test", "Type 1")
    source2 = AuthoritySource("AUTH-002", "Authority 2", "Test", "Type 2")
    
    inv.add_authority_source(source1)
    inv.add_authority_source(source2)
    inv.add_connection("AUTH-001", "AUTH-002")
    
    assert "AUTH-002" in inv.sources["AUTH-001"].connections
    assert "AUTH-001" in inv.sources["AUTH-002"].connections
    print("✓ Add connections test passed")


def test_add_notes():
    """Test adding investigation notes."""
    inv = Investigation("INV-TEST", "Test", "Test investigation")
    
    inv.add_note("First note")
    inv.add_note("Second note")
    
    assert len(inv.notes) == 2
    assert inv.notes[0]['note'] == "First note"
    assert inv.notes[1]['note'] == "Second note"
    print("✓ Add notes test passed")


def test_desk_operations():
    """Test InvestigatorDesk operations."""
    # Create temporary directory for test data
    test_dir = tempfile.mkdtemp()
    
    try:
        desk = InvestigatorDesk(data_dir=test_dir)
        
        # Create investigation
        inv = desk.create_investigation(
            "INV-DESK-TEST",
            "Desk Test",
            "Testing desk operations"
        )
        
        assert inv.investigation_id == "INV-DESK-TEST"
        assert "INV-DESK-TEST" in desk.investigations
        
        # Verify file was created
        expected_file = os.path.join(test_dir, "INV-DESK-TEST.json")
        assert os.path.exists(expected_file)
        
        # Test retrieval
        retrieved = desk.get_investigation("INV-DESK-TEST")
        assert retrieved is not None
        assert retrieved.title == "Desk Test"
        
        # Test listing
        all_invs = desk.list_investigations()
        assert len(all_invs) == 1
        
        print("✓ Desk operations test passed")
        
    finally:
        # Cleanup
        shutil.rmtree(test_dir)


def test_serialization():
    """Test investigation serialization and deserialization."""
    # Create investigation with data
    inv = Investigation("INV-SER", "Serialization Test", "Testing serialization")
    source = AuthoritySource("AUTH-001", "Test Authority", "Test", "Type")
    inv.add_authority_source(source)
    inv.add_evidence("AUTH-001", "Doc", "Evidence", "Ref")
    inv.add_note("Test note")
    
    # Serialize
    data = inv.to_dict()
    
    # Deserialize
    inv2 = Investigation.from_dict(data)
    
    assert inv2.investigation_id == inv.investigation_id
    assert inv2.title == inv.title
    assert len(inv2.sources) == 1
    assert len(inv2.notes) == 1
    assert "AUTH-001" in inv2.sources
    assert len(inv2.sources["AUTH-001"].evidence) == 1
    
    print("✓ Serialization test passed")


def test_report_generation():
    """Test investigation report generation."""
    test_dir = tempfile.mkdtemp()
    
    try:
        desk = InvestigatorDesk(data_dir=test_dir)
        inv = desk.create_investigation("INV-REP", "Report Test", "Testing reports")
        
        source = AuthoritySource("AUTH-001", "Test Authority", "Test", "Type")
        inv.add_authority_source(source)
        inv.add_evidence("AUTH-001", "Doc", "Test evidence", "Ref")
        inv.add_note("Test note")
        desk.save_investigation(inv)
        
        report = desk.generate_report("INV-REP")
        
        assert "Report Test" in report
        assert "AUTH-001" in report
        assert "Test Authority" in report
        assert "Test evidence" in report
        assert "Test note" in report
        
        print("✓ Report generation test passed")
        
    finally:
        shutil.rmtree(test_dir)


def run_tests():
    """Run all tests."""
    print("=" * 70)
    print("Running INVESTIGATOR-DESK Tests")
    print("=" * 70)
    print()
    
    tests = [
        test_authority_source_creation,
        test_investigation_creation,
        test_add_authority_source,
        test_add_evidence,
        test_add_connections,
        test_add_notes,
        test_desk_operations,
        test_serialization,
        test_report_generation,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    if failed == 0:
        print(f"All {len(tests)} tests passed! ✓")
        print("=" * 70)
        return 0
    else:
        print(f"{failed}/{len(tests)} tests failed.")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
