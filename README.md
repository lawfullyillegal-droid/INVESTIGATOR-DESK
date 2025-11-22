# INVESTIGATOR-DESK

**An Investigation App That Targets the Source of Authority**

INVESTIGATOR-DESK is a powerful investigation tool designed to help investigators track, analyze, and document sources of authority. Whether you're investigating corporate hierarchies, governmental structures, or organizational power dynamics, this app provides the tools you need to map authority relationships and gather evidence.

## Features

- 📊 **Authority Source Tracking**: Document and track different sources of authority
- 🔍 **Evidence Management**: Attach evidence to each authority source with proper documentation
- 🔗 **Connection Mapping**: Visualize relationships and connections between authority sources
- 📝 **Investigation Notes**: Maintain detailed notes throughout your investigation
- 📄 **Comprehensive Reports**: Generate detailed investigation reports
- 💾 **Persistent Storage**: All investigation data is saved locally in JSON format

## Installation

### Requirements

- Python 3.6 or higher

### Setup

1. Clone this repository:
```bash
git clone https://github.com/lawfullyillegal-droid/INVESTIGATOR-DESK.git
cd INVESTIGATOR-DESK
```

2. Make the script executable (optional):
```bash
chmod +x investigator.py
```

## Usage

### Running the Application

```bash
python3 investigator.py
```

The application will:
1. Create a sample investigation demonstrating the core functionality
2. Display a comprehensive report of the investigation
3. Save all data to the `.investigator-data` directory

### Sample Output

The app includes a demonstration investigation that tracks a corporate authority structure, showing:
- Multiple authority sources (CEO, Board of Directors, CFO)
- Evidence linking each source to their authority
- Connections between authority sources
- Investigation notes and timestamps

### Using as a Library

You can also import and use INVESTIGATOR-DESK in your own Python scripts:

```python
from investigator import InvestigatorDesk, Investigation, AuthoritySource

# Initialize the desk
desk = InvestigatorDesk()

# Create an investigation
inv = desk.create_investigation(
    "INV-002",
    "Government Authority Investigation",
    "Investigating governmental authority structure"
)

# Add authority sources
president = AuthoritySource(
    "AUTH-PRES",
    "President",
    "Chief executive authority",
    "Executive Branch"
)
inv.add_authority_source(president)

# Add evidence
inv.add_evidence(
    "AUTH-PRES",
    "Constitutional Authority",
    "Article II grants executive power",
    "U.S. Constitution Article II"
)

# Save the investigation
desk.save_investigation(inv)

# Generate a report
report = desk.generate_report("INV-002")
print(report)
```

## Data Structure

### Authority Sources

Each authority source includes:
- **ID**: Unique identifier
- **Name**: Display name
- **Description**: Detailed description
- **Type**: Category of authority (Executive, Governance, etc.)
- **Evidence**: List of supporting evidence
- **Connections**: Related authority sources

### Investigations

Each investigation contains:
- **ID**: Unique investigation identifier
- **Title**: Investigation title
- **Description**: Investigation description
- **Status**: Current status (active, closed, etc.)
- **Sources**: Collection of authority sources
- **Notes**: Timestamped investigation notes

## Data Storage

All investigation data is stored in the `.investigator-data` directory as JSON files. Each investigation is saved separately, making it easy to:
- Back up investigations
- Share investigation data
- Version control your research

## Use Cases

- **Corporate Investigations**: Map organizational hierarchies and authority structures
- **Legal Research**: Document chains of authority for legal cases
- **Academic Research**: Study power structures in institutions
- **Compliance Audits**: Track decision-making authority and accountability
- **Investigative Journalism**: Document authority relationships in complex stories

## Contributing

This is an investigation tool designed to help uncover and document sources of authority. Contributions that enhance investigation capabilities are welcome.

## License

This project is provided as-is for investigative and research purposes.

## Target

**INVESTIGATE THE SOURCE OF AUTHORITY**

This tool empowers investigators to systematically identify, document, and analyze sources of authority in any organizational or governmental context.
