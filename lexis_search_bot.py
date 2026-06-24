#!/usr/bin/env python3
"""
LEXIS-STYLE LEGAL SEARCH BOT FOR INVESTIGATOR-DESK

Integrates free/public legal research databases with the InvestigatorDesk framework.
Searches CourtListener, Google Scholar, and other public legal resources.

Usage:
    from lexis_search_bot import LegalSearchBot
    from investigator import InvestigatorDesk
    
    bot = LegalSearchBot()
    desk = InvestigatorDesk()
    inv = desk.create_investigation("INV-002", "Case Research", "Legal case investigation")
    
    # Search and auto-add to investigation
    bot.search_and_add(inv, query="Miranda v Arizona", source_type="case")
    desk.save_investigation(inv)
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import quote_plus
import sys
import os

# Import from investigator.py if available
try:
    from investigator import AuthoritySource, Investigation
except ImportError:
    print("Warning: investigator.py not found. AuthoritySource/Investigation classes unavailable.", file=sys.stderr)
    AuthoritySource = None
    Investigation = None


class LegalSearchBot:
    """
    Free/public legal research search bot.
    Searches CourtListener, Google Scholar, and public court databases.
    """
    
    COURTLISTENER_API = "https://www.courtlistener.com/api/rest/v3"
    GOOGLE_SCHOLAR_BASE = "https://scholar.google.com/scholar"
    
    def __init__(self, courtlistener_token: Optional[str] = None, rate_limit: float = 1.0):
        """
        Initialize the legal search bot.
        
        Args:
            courtlistener_token: Optional CourtListener API token (free registration)
            rate_limit: Seconds to wait between requests (default 1.0)
        """
        self.courtlistener_token = courtlistener_token
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'LawfullyIllegal-INVESTIGATOR-DESK/1.0 (Legal Research Bot)'
        })
        
        if self.courtlistener_token:
            self.session.headers.update({
                'Authorization': f'Token {self.courtlistener_token}'
            })
    
    def _rate_limit_wait(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()
    
    def search_courtlistener_cases(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search CourtListener for legal cases.
        
        Args:
            query: Search query string
            limit: Maximum number of results
        
        Returns:
            List of case dictionaries with metadata
        """
        self._rate_limit_wait()
        
        try:
            url = f"{self.COURTLISTENER_API}/search/"
            params = {
                'q': query,
                'type': 'o',  # opinions
                'order_by': 'score desc',
                'page_size': min(limit, 20)
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('results', [])[:limit]:
                    results.append({
                        'source': 'CourtListener',
                        'case_name': item.get('caseName', 'Unknown'),
                        'court': item.get('court', 'Unknown'),
                        'date_filed': item.get('dateFiled', 'Unknown'),
                        'citation': item.get('citation', []),
                        'snippet': item.get('snippet', ''),
                        'url': f"https://www.courtlistener.com{item.get('absolute_url', '')}",
                        'docket_number': item.get('docketNumber', ''),
                        'status': item.get('status', '')
                    })
                
                return results
            else:
                print(f"CourtListener API error: {response.status_code}", file=sys.stderr)
                return []
                
        except Exception as e:
            print(f"Error searching CourtListener: {e}", file=sys.stderr)
            return []
    
    def search_google_scholar_cases(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search Google Scholar for legal cases (scraping-free metadata only).
        
        Note: Returns search URL for manual review. Google Scholar blocks automated scraping.
        
        Args:
            query: Search query
            limit: Not used (included for API consistency)
        
        Returns:
            List with single item containing search URL
        """
        search_url = f"{self.GOOGLE_SCHOLAR_BASE}?q={quote_plus(query)}&hl=en&as_sdt=6"
        
        return [{
            'source': 'Google Scholar',
            'query': query,
            'url': search_url,
            'note': 'Manual review required - Google Scholar blocks automated access',
            'timestamp': datetime.now().isoformat()
        }]
    
    def search_courtlistener_dockets(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search CourtListener for dockets/filings.
        
        Args:
            query: Search query
            limit: Maximum results
        
        Returns:
            List of docket dictionaries
        """
        self._rate_limit_wait()
        
        try:
            url = f"{self.COURTLISTENER_API}/search/"
            params = {
                'q': query,
                'type': 'r',  # dockets
                'order_by': 'score desc',
                'page_size': min(limit, 20)
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('results', [])[:limit]:
                    results.append({
                        'source': 'CourtListener',
                        'type': 'docket',
                        'case_name': item.get('caseName', 'Unknown'),
                        'court': item.get('court', 'Unknown'),
                        'docket_number': item.get('docketNumber', ''),
                        'date_filed': item.get('dateFiled', ''),
                        'url': f"https://www.courtlistener.com{item.get('absolute_url', '')}",
                        'snippet': item.get('snippet', '')
                    })
                
                return results
            else:
                print(f"CourtListener docket search error: {response.status_code}", file=sys.stderr)
                return []
                
        except Exception as e:
            print(f"Error searching dockets: {e}", file=sys.stderr)
            return []
    
    def search_all_sources(self, query: str, include_scholar: bool = False, limit: int = 10) -> Dict[str, List]:
        """
        Search all available legal databases.
        
        Args:
            query: Search query
            include_scholar: Include Google Scholar (manual review only)
            limit: Max results per source
        
        Returns:
            Dictionary with results from each source
        """
        results = {
            'cases': self.search_courtlistener_cases(query, limit),
            'dockets': self.search_courtlistener_dockets(query, limit)
        }
        
        if include_scholar:
            results['scholar'] = self.search_google_scholar_cases(query, limit)
        
        return results
    
    def create_authority_source_from_case(self, case: Dict, source_id_prefix: str = "CASE") -> 'AuthoritySource':
        """
        Convert a case search result to an AuthoritySource object.
        
        Args:
            case: Case dictionary from search results
            source_id_prefix: Prefix for source ID
        
        Returns:
            AuthoritySource object
        """
        if AuthoritySource is None:
            raise ImportError("AuthoritySource class not available. Ensure investigator.py is in the same directory.")
        
        # Generate unique source ID
        case_name = case.get('case_name', 'Unknown')
        safe_name = ''.join(c if c.isalnum() else '_' for c in case_name)[:30]
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        source_id = f"{source_id_prefix}-{safe_name}-{timestamp}"
        
        # Build description
        description = f"{case.get('court', 'Unknown Court')} - {case.get('date_filed', 'Date Unknown')}"
        if case.get('docket_number'):
            description += f" | Docket: {case['docket_number']}"
        if case.get('citation'):
            citations = case['citation'] if isinstance(case['citation'], list) else [case['citation']]
            description += f" | Citations: {', '.join(citations)}"
        
        # Create AuthoritySource
        source = AuthoritySource(
            source_id=source_id,
            name=case_name,
            description=description,
            authority_type="Case Law"
        )
        
        # Add evidence
        source.evidence.append({
            'type': 'Legal Research',
            'description': case.get('snippet', 'No snippet available'),
            'source': f"{case.get('source', 'Unknown')} - {case.get('url', 'No URL')}",
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'court': case.get('court'),
                'date_filed': case.get('date_filed'),
                'docket_number': case.get('docket_number'),
                'status': case.get('status')
            }
        })
        
        return source
    
    def search_and_add(self, investigation: 'Investigation', query: str, 
                       source_type: str = "case", limit: int = 5) -> int:
        """
        Search legal databases and automatically add results to an investigation.
        
        Args:
            investigation: Investigation object to add sources to
            query: Search query
            source_type: Type of search ('case', 'docket', 'all')
            limit: Maximum results to add
        
        Returns:
            Number of sources added
        """
        if Investigation is None:
            raise ImportError("Investigation class not available. Ensure investigator.py is in the same directory.")
        
        added_count = 0
        
        if source_type == "case" or source_type == "all":
            cases = self.search_courtlistener_cases(query, limit)
            for case in cases:
                try:
                    source = self.create_authority_source_from_case(case, "CASE")
                    investigation.add_authority_source(source)
                    added_count += 1
                except Exception as e:
                    print(f"Error adding case source: {e}", file=sys.stderr)
        
        if source_type == "docket" or source_type == "all":
            dockets = self.search_courtlistener_dockets(query, limit)
            for docket in dockets:
                try:
                    source = self.create_authority_source_from_case(docket, "DOCKET")
                    investigation.add_authority_source(source)
                    added_count += 1
                except Exception as e:
                    print(f"Error adding docket source: {e}", file=sys.stderr)
        
        # Add investigation note
        investigation.add_note(
            f"Legal search completed: '{query}' | Type: {source_type} | {added_count} sources added | " 
            f"Bot: LexisSearchBot v1.0"
        )
        
        return added_count


def demo():
    """Demonstration of LegalSearchBot functionality."""
    print("="*70)
    print("LEXIS-STYLE LEGAL SEARCH BOT - DEMONSTRATION")
    print("="*70)
    print()
    
    bot = LegalSearchBot()
    
    # Test search
    print("Searching CourtListener for: 'Miranda v Arizona'...")
    cases = bot.search_courtlistener_cases("Miranda v Arizona", limit=3)
    
    print(f"\nFound {len(cases)} cases:\n")
    for i, case in enumerate(cases, 1):
        print(f"{i}. {case['case_name']}")
        print(f"   Court: {case['court']}")
        print(f"   Date: {case['date_filed']}")
        print(f"   URL: {case['url']}")
        print()
    
    # Test all sources
    print("-"*70)
    print("Searching all sources for: 'Fourth Amendment search'...")
    all_results = bot.search_all_sources("Fourth Amendment search", limit=2)
    
    print(f"\nCases: {len(all_results['cases'])}")
    print(f"Dockets: {len(all_results['dockets'])}")
    print()
    
    # Integration test (if investigator.py available)
    if Investigation and AuthoritySource:
        print("-"*70)
        print("Testing integration with InvestigatorDesk...")
        
        try:
            from investigator import InvestigatorDesk
            
            desk = InvestigatorDesk()
            inv = desk.create_investigation(
                "LEGAL-DEMO-001",
                "Legal Research Demo",
                "Demonstration of automated legal research integration"
            )
            
            added = bot.search_and_add(inv, "habeas corpus", source_type="case", limit=2)
            desk.save_investigation(inv)
            
            print(f"✓ Created investigation: {inv.investigation_id}")
            print(f"✓ Added {added} case law sources")
            print(f"✓ Saved to: {desk.data_dir}")
            
        except Exception as e:
            print(f"Integration test failed: {e}")
    else:
        print("\nSkipping integration test (investigator.py not found)")
    
    print("\n" + "="*70)
    print("Demo complete!")
    print("="*70)


if __name__ == "__main__":
    demo()
