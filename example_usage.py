#!/usr/bin/env python3
"""
Example usage of INVESTIGATOR-DESK for a government authority investigation.
This demonstrates how to use the app as a library for custom investigations.
"""

from investigator import InvestigatorDesk, AuthoritySource

def main():
    # Initialize the desk
    desk = InvestigatorDesk()
    
    # Create a new investigation
    print("Creating investigation: Government Executive Authority")
    inv = desk.create_investigation(
        "INV-GOV-001",
        "Executive Branch Authority Investigation",
        "Investigating the sources and limits of executive authority in government"
    )
    
    # Add authority sources
    print("Adding authority sources...")
    
    president = AuthoritySource(
        "AUTH-PRESIDENT",
        "Office of the President",
        "Chief executive officer of the nation with constitutional authority",
        "Executive Branch"
    )
    inv.add_authority_source(president)
    
    congress = AuthoritySource(
        "AUTH-CONGRESS",
        "United States Congress",
        "Legislative branch with authority to create laws",
        "Legislative Branch"
    )
    inv.add_authority_source(congress)
    
    supreme_court = AuthoritySource(
        "AUTH-SCOTUS",
        "Supreme Court",
        "Judicial branch with authority to interpret laws and constitution",
        "Judicial Branch"
    )
    inv.add_authority_source(supreme_court)
    
    constitution = AuthoritySource(
        "AUTH-CONSTITUTION",
        "U.S. Constitution",
        "Foundational document establishing governmental authority",
        "Constitutional"
    )
    inv.add_authority_source(constitution)
    
    # Add evidence for each authority source
    print("Adding evidence...")
    
    inv.add_evidence(
        "AUTH-PRESIDENT",
        "Constitutional Grant",
        "Article II vests executive power in the President",
        "U.S. Constitution, Article II, Section 1"
    )
    
    inv.add_evidence(
        "AUTH-PRESIDENT",
        "Limited Powers",
        "Presidential powers subject to checks and balances",
        "U.S. Constitution, Articles I-III"
    )
    
    inv.add_evidence(
        "AUTH-CONGRESS",
        "Constitutional Grant",
        "Article I vests all legislative powers in Congress",
        "U.S. Constitution, Article I, Section 1"
    )
    
    inv.add_evidence(
        "AUTH-CONGRESS",
        "Enumerated Powers",
        "Congress has specific enumerated powers and implied powers",
        "U.S. Constitution, Article I, Section 8"
    )
    
    inv.add_evidence(
        "AUTH-SCOTUS",
        "Constitutional Grant",
        "Article III establishes judicial power in Supreme Court",
        "U.S. Constitution, Article III, Section 1"
    )
    
    inv.add_evidence(
        "AUTH-SCOTUS",
        "Judicial Review",
        "Established power to review constitutionality of laws",
        "Marbury v. Madison (1803)"
    )
    
    inv.add_evidence(
        "AUTH-CONSTITUTION",
        "Popular Sovereignty",
        "We the People establish the Constitution",
        "U.S. Constitution, Preamble"
    )
    
    inv.add_evidence(
        "AUTH-CONSTITUTION",
        "Amendment Process",
        "Constitution can be amended by the People through their representatives",
        "U.S. Constitution, Article V"
    )
    
    # Establish connections between authorities
    print("Mapping authority connections...")
    
    inv.add_connection("AUTH-CONSTITUTION", "AUTH-PRESIDENT")
    inv.add_connection("AUTH-CONSTITUTION", "AUTH-CONGRESS")
    inv.add_connection("AUTH-CONSTITUTION", "AUTH-SCOTUS")
    inv.add_connection("AUTH-PRESIDENT", "AUTH-CONGRESS")
    inv.add_connection("AUTH-CONGRESS", "AUTH-SCOTUS")
    
    # Add investigation notes
    print("Adding investigation notes...")
    
    inv.add_note("System of checks and balances identified across three branches")
    inv.add_note("Constitution identified as ultimate source of governmental authority")
    inv.add_note("Constitution derives authority from 'We the People' - popular sovereignty")
    inv.add_note("All three branches have constitutional limits on their authority")
    inv.add_note("Investigation reveals distributed authority rather than centralized power")
    
    # Save the investigation
    desk.save_investigation(inv)
    
    # Generate and display the report
    print("\n" + "=" * 70)
    print("INVESTIGATION COMPLETE - Generating Report")
    print("=" * 70 + "\n")
    
    report = desk.generate_report("INV-GOV-001")
    print(report)
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("The investigation reveals that governmental authority in the United States")
    print("is derived from the Constitution, which itself derives authority from the")
    print("People. Authority is distributed across three co-equal branches with a")
    print("system of checks and balances preventing concentration of power.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
