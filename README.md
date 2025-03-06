# Fake Frenzy 

A powerful and creative fake data generation tool powered by Google's Gemini AI. Generate realistic, fantasy, and story-based data with an intuitive interface.
# The Deployment - https://fakefrenzy.onrender.com/

## The problems i faced - 

### the ui - this is something im a little bit behind in i.e frontend so had to use perplexity and cursor ai to come up and develop the theme.

## the issues that havent been resolved - 

### the export button : it works on my local host but when deployed it doesnt still working on that.
### the video demo of export - https://youtu.be/XtGrY-Pr8p0

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Details](#technical-details)
- [Modes](#modes)
- [Data Management](#data-management)
- [Export Options](#export-options)
- [Customization](#customization)
- [API Integration](#api-integration)
- [UI/UX Design](#uiux-design)
- [Error Handling](#error-handling)
- [Contributing](#contributing)

## Overview

Fake Frenzy is a sophisticated web application that leverages Google's Gemini AI to generate various types of fake data. Whether you need realistic personal information, fantasy characters, or engaging stories, Fake Frenzy provides a user-friendly interface to create and manage generated data.


## Features

### Core Functionality
- Multiple generation modes (Regular, Fantasy, Story)
- Batch generation support (up to 10 entries)
- Favorites system for saving interesting entries
- History tracking with timestamps
- Export capabilities (JSON, CSV, SQL)
- Surprise generation for unexpected results

### Generation Modes

#### Regular Mode
- Full names
- Email addresses
- Physical addresses
- Phone numbers
- Occupations

#### Fantasy Mode
1. **Time Travel**
   - Ancient (3000 BC - 500 AD)
   - Medieval (500 - 1500)
   - Renaissance (1300 - 1700)
   - Victorian (1837 - 1901)
   - Modern (1901 - Present)
   - Future (2100+)

2. **Character Universe**
   - Royal Family
   - Magical Academy
   - Adventurer Guild
   - Mythical Creatures
   - Ancient Gods

3. **Alternate Reality**
   - Steampunk
   - Cyberpunk
   - Post-Apocalyptic
   - Utopian
   - Magical Realism

#### Story Mode
- Character-based storytelling
- Multiple chapters
- Epilogue generation
- Rich narrative details

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SoumitraDeshpande11/FakeFrenzy.git
cd fake-frenzy
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file
touch .env

# Add your Gemini API key
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Access the web interface:
```
http://localhost:8080
```

## Technical Details

### Dependencies
- NiceGUI: Web interface framework
- Google Generative AI: Gemini API integration
- Python-dotenv: Environment variable management
- JSON: Data formatting
- CSV: Export functionality
- SQLite: Database export support

### File Structure
```
fake-frenzy/
├── main.py           # Main application file
├── .env              # Environment variables
├── requirements.txt  # Project dependencies
├── README.md        # Documentation
└── exports/         # Generated data files
```

### Key Components

#### Data Generation
- `generate_fake_data()`: Regular data generation
- `generate_fantasy_data()`: Fantasy mode generation
- `generate_character_story()`: Story mode generation
- `generate_surprise_data()`: Surprise data generation

#### UI Components
- `main_page()`: Main interface layout
- `show_data_dialog()`: Data display dialog
- `refresh_containers()`: UI update mechanism

#### Data Management
- `save_to_favorites()`: Favorites system
- `add_to_history()`: History tracking
- `export_data()`: Data export

## Modes

### Regular Mode
Generates realistic personal information using structured prompts to ensure consistency and validity.

### Fantasy Mode
Implements three sub-modes with specific characteristics:

1. **Time Travel**
   - Era-appropriate names and titles
   - Historical accuracy in occupations
   - Period-specific locations

2. **Character Universe**
   - Interconnected character relationships
   - Consistent universe rules
   - Themed attributes and equipment

3. **Alternate Reality**
   - Genre-specific details
   - Unique world-building elements
   - Specialized occupations and traits

### Story Mode
Creates narrative content with:
- Character background integration
- Multi-chapter structure
- Consistent storytelling
- Dynamic epilogue generation

## Data Management

### Favorites System
- Add/remove entries
- Persistent storage
- Quick access interface
- Categorized viewing

### History Tracking
- Timestamp recording
- Entry type logging
- Configurable history size
- Clear history option

## Export Options

### JSON Format
```json
{
    "people": [
        {
            "full_name": "...",
            "email": "...",
            "address": "...",
            "phone_number": "...",
            "occupation": "..."
        }
    ]
}
```

### CSV Format
- Header row inclusion
- Standard CSV formatting
- Field separation
- Quote handling

### SQL Format
- Table creation scripts
- INSERT statements
- SQLite compatibility
- Data type handling

## Customization

### Settings Panel
- Export format selection
- History size configuration
- UI preferences
- Generation options

### Theme
- Paper-style interface
- Responsive design
- Custom CSS styling
- Dialog animations

## API Integration

### Gemini AI
- Prompt engineering
- Response parsing
- Error handling
- Rate limiting

### Data Processing
- JSON validation
- Format conversion
- Data cleaning
- Structure verification

## UI/UX Design

### Components
- Tabbed interface
- Modal dialogs
- Responsive containers
- Interactive buttons

### Styling
- Custom CSS classes
- Material Design icons
- Consistent theming
- Visual feedback

## Error Handling

### Types
- API errors
- Data validation
- Format conversion
- User input

### Recovery
- Fallback options
- User notifications
- Graceful degradation
- Debug logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Open a Pull Request

### Guidelines
- Follow PEP 8 style guide
- Add comprehensive comments
- Include error handling
- Update documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
