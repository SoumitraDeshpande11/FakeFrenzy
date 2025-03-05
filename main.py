from nicegui import ui
import os
from dotenv import load_dotenv
import json
import google.generativeai as genai
from datetime import datetime
import csv
import asyncio

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Use the latest Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Global variable for number of entries
num_entries = 1  # Default number of entries to generate

# Global variables for features
saved_favorites = []
generation_history = []
export_format = 'json'  # Default export format
max_history_entries = 50  # Default max history entries

# Add these global variables at the top with other globals
favorites_container = None
history_container = None

# Add these global variables at the top with other globals
mode = None
fantasy_type_select = None
era = None
universe_type = None
reality_type = None

# Add this at the top of the file with other imports and globals
paper_style = '''
<style>
body { 
    background-color: #f7f1e3 !important; 
    background-image: url("data:image/png;base64,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");
    color: #2c1810; 
    font-family: 'Comic Sans MS', cursive, sans-serif;
}
.nicegui-content {
    background: transparent !important;
}
button { 
    background-color: #8b4513 !important; 
    color: #f7f1e3 !important; 
    border: 2px solid #5c2e0e !important;
    padding: 10px 20px;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    transition: all 0.3s ease;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    font-weight: bold;
}
button:hover { 
    background-color: #a0522d !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.text-h4 { 
    color: #8b4513;
    font-size: 2.5em !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    font-weight: bold;
    margin-bottom: 1em;
}
.text-h6 { 
    color: #8b4513;
    font-weight: bold;
}
.dialog, .card { 
    background: transparent !important;
    color: #2c1810;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(139, 69, 19, 0.2);
    border: 2px solid #d2b48c;
    backdrop-filter: brightness(1.02);
}
.separator {
    background-color: #d2b48c;
    height: 2px !important;
    opacity: 0.6;
}
.number-input {
    background-color: transparent !important;
    border: 2px solid #d2b48c !important;
    border-radius: 8px;
    color: #2c1810;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    padding: 8px !important;
}
.number-input:focus {
    border-color: #8b4513 !important;
    box-shadow: 0 0 0 2px rgba(139, 69, 19, 0.2);
}
label {
    color: #5c2e0e !important;
    font-weight: bold;
    font-size: 1.1em;
}
select, .select {
    background-color: transparent !important;
    border: 2px solid #d2b48c !important;
    border-radius: 8px;
    color: #2c1810 !important;
    font-family: 'Comic Sans MS', cursive, sans-serif;
}
.select-options {
    background-color: #f7f1e3 !important;
    border: 2px solid #d2b48c !important;
    color: #2c1810 !important;
}

/* Make all containers transparent */
.q-tab-panels,
.q-tab-panel,
.scroll-area,
.q-scrollarea,
.q-card {
    background: transparent !important;
}

/* Style the tabs */
.q-tabs {
    background: transparent !important;
}

.q-tab {
    color: #8b4513 !important;
    font-family: 'Comic Sans MS', cursive, sans-serif;
}

.q-tab--active {
    color: #5c2e0e !important;
    font-weight: bold;
}

/* Style scrollbars */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background-color: #d2b48c;
    border-radius: 4px;
    border: 2px solid transparent;
}

/* Make all panels and containers transparent */
.q-panel,
.q-tab-panels,
.q-tab-panel,
.nicegui-content > div {
    background: transparent !important;
}

/* Make all dialog and modal content transparent */
.q-dialog,
.q-dialog__inner,
.q-dialog__inner > div,
.dialog-content,
.q-card__section {
    background: transparent !important;
}

/* Dialog content with darker border */
.dialog-content {
    background-color: #f7f1e3 !important;
    background-image: url("data:image/png;base64,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");
    border: 2px solid #2c1810 !important;  /* Darker border color */
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(44, 24, 16, 0.3);  /* Darker shadow */
    animation: dialogFadeIn 0.3s ease;
}

/* Add inner border for more definition */
.dialog-content::before {
    content: '';
    position: absolute;
    top: 4px;
    left: 4px;
    right: 4px;
    bottom: 4px;
    border: 1px solid #8b4513;
    border-radius: 10px;
    pointer-events: none;
}

/* Update separator style */
.dialog-content .separator {
    background-color: #2c1810;
    height: 1px !important;
    opacity: 0.3;
    margin: 1rem 0;
}

/* Style dialog text */
.dialog-content label {
    color: #2c1810 !important;
    font-family: 'Comic Sans MS', cursive, sans-serif;
}

/* Style dialog title */
.dialog-content .text-h6 {
    color: #8b4513;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

/* Style dialog backdrop */
.q-dialog__backdrop {
    background: rgba(139, 69, 19, 0.1) !important;
    backdrop-filter: blur(4px) !important;
    -webkit-backdrop-filter: blur(4px) !important;
    transition: backdrop-filter 0.3s ease;
}

/* Style dialog scrollbar */
.dialog-content ::-webkit-scrollbar {
    width: 8px;
}

.dialog-content ::-webkit-scrollbar-track {
    background: transparent;
}

.dialog-content ::-webkit-scrollbar-thumb {
    background-color: #d2b48c;
    border-radius: 4px;
}

/* Animation for dialog appearance */
@keyframes dialogFadeIn {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Make the main content slightly blurred when dialog is open */
body.q-dialog--modal {
    overflow: hidden;
}

.q-dialog--modal .nicegui-content {
    filter: blur(4px);
    transition: filter 0.3s ease;
}

/* Style the main title */
.text-h3 {
    color: #8b4513;
    font-size: 3em !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    font-weight: 900 !important;
    margin-bottom: 0.2em;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    letter-spacing: 1px;
}

/* Style the subtitle */
.text-subtitle1 {
    color: #5c2e0e;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    font-size: 1.2em !important;
}
</style>
'''

# Add this function definition before main_page
def show_data_dialog(data, mode='Regular'):
    with ui.dialog() as dialog, ui.card().classes('w-96 dialog-content'):
        # Add header with title and favorite button
        with ui.row().classes('w-full justify-between items-center mb-4'):
            title = '🎲 Generated Data' if mode == 'Regular' else '✨ Fantasy Data' if mode == 'Fantasy Mode' else '📖 Story Mode'
            ui.label(title).classes('text-h6')
            ui.button(icon='favorite', on_click=lambda: save_to_favorites(data)).classes(
                'text-red-500 bg-transparent hover:bg-red-50'
            ).tooltip('Add to Favorites')

        with ui.column().classes('max-h-96 overflow-auto'):
            if mode == 'Regular':
                for i, person in enumerate(data.get('people', [])):
                    ui.label(f"Person {i+1}:").classes('text-h6 mt-4')
                    ui.label(f"Name: {person.get('full_name')}").classes('mt-2')
                    ui.label(f"Email: {person.get('email')}").classes('mt-2')
                    ui.label(f"Address: {person.get('address')}").classes('mt-2')
                    ui.label(f"Phone: {person.get('phone_number')}").classes('mt-2')
                    ui.label(f"Occupation: {person.get('occupation')}").classes('mt-2')
                    if i < len(data.get('people')) - 1:
                        ui.separator().classes('my-4')
            
            elif mode == 'Fantasy Mode':
                for i, person in enumerate(data.get('people', [])):
                    ui.label(f"{person.get('title', 'Character')} {i+1}:").classes('text-h6 mt-4')
                    ui.label(f"Name: {person.get('full_name')}").classes('mt-2')
                    ui.label(f"Title: {person.get('title')}").classes('mt-2')
                    ui.label(f"Age: {person.get('age')}").classes('mt-2')
                    ui.label(f"Origin: {person.get('origin')}").classes('mt-2')
                    ui.label(f"Occupation: {person.get('occupation')}").classes('mt-2')
                    
                    if person.get('special_traits'):
                        ui.label('Special Traits:').classes('mt-2 font-bold')
                        for trait in person['special_traits']:
                            ui.label(f"• {trait}").classes('ml-4')
                    
                    if person.get('equipment'):
                        ui.label('Equipment:').classes('mt-2 font-bold')
                        for item in person['equipment']:
                            ui.label(f"• {item}").classes('ml-4')
                    
                    if person.get('relationships'):
                        ui.label('Relationships:').classes('mt-2 font-bold')
                        for rel in person['relationships']:
                            ui.label(f"• {rel['type']} to {rel['to']}").classes('ml-4')
                    
                    ui.label('Backstory:').classes('mt-2 font-bold')
                    ui.label(person.get('backstory')).classes('ml-4')
                    
                    if i < len(data.get('people')) - 1:
                        ui.separator().classes('my-4')
            
            elif mode == 'Story Mode':
                if 'story' in data:
                    story = data['story']
                    ui.label(story.get('title', 'Story')).classes('text-h5 mb-4')
                    for chapter in story.get('chapters', []):
                        ui.label(chapter.get('heading', 'Chapter')).classes('text-h6 mt-4')
                        ui.label(chapter.get('content', '')).classes('mt-2')
                        ui.separator().classes('my-4')
                    if story.get('epilogue'):
                        ui.label('Epilogue').classes('text-h6 mt-4')
                        ui.label(story['epilogue']).classes('mt-2')

        # Footer with close button
        with ui.row().classes('w-full justify-between mt-4'):
            ui.button('Close', on_click=dialog.close)
            ui.button(
                'Add to Favorites', 
                on_click=lambda: [save_to_favorites(data), dialog.close()]
            ).classes('bg-red-600')
        dialog.open()

# Update the main_page function
def main_page():
    global mode, fantasy_type_select, era, universe_type, reality_type
    ui.html(paper_style)
    
    with ui.column().classes('w-full items-center gap-2'):
        ui.label('Fake Frenzy').classes('text-h3 text-center font-bold')
        ui.label('Generate Fun & Creative Fake Data').classes('text-subtitle1 text-center mb-4 opacity-75')
    
    # Add tabs
    with ui.tabs().classes('w-full justify-center') as tabs:
        ui.tab('Generate', icon='add')
        ui.tab('Favorites', icon='star')
        ui.tab('History', icon='history')
        ui.tab('Settings', icon='settings')
    
    with ui.tab_panels(tabs, value='Generate').classes('w-full'):
        with ui.tab_panel('Generate'):
            # Generation panel
            with ui.column().classes('w-full items-center gap-4'):
                # Add mode selector
                mode = ui.select(
                    options=[
                        'Regular',
                        'Fantasy Mode',
                        'Story Mode'
                    ],
                    value='Regular',
                    label='Generation Mode'
                ).classes('w-48 mb-4')

                # Add sub-mode for Fantasy
                fantasy_container = ui.column().classes('w-full items-center gap-2')
                fantasy_container.bind_visibility_from(mode, 'value', lambda x: x == 'Fantasy Mode')

                with fantasy_container:
                    fantasy_type_select = ui.select(
                        options=[
                            'Time Travel',
                            'Character Universe',
                            'Alternate Reality'
                        ],
                        value='Time Travel',
                        label='Fantasy Type'
                    ).classes('w-48 mb-2')
                    
                    # Time Travel specific options
                    time_travel_container = ui.column().classes('w-full items-center gap-2')
                    time_travel_container.bind_visibility_from(fantasy_type_select, 'value', lambda x: x == 'Time Travel')
                    
                    with time_travel_container:
                        era = ui.select(
                            options=[
                                'Ancient (3000 BC - 500 AD)',
                                'Medieval (500 - 1500)',
                                'Renaissance (1300 - 1700)',
                                'Victorian (1837 - 1901)',
                                'Modern (1901 - Present)',
                                'Future (2100+)'
                            ],
                            value='Medieval (500 - 1500)',
                            label='Time Period'
                        ).classes('w-48')

                    # Character Universe specific options
                    universe_container = ui.column().classes('w-full items-center gap-2')
                    universe_container.bind_visibility_from(fantasy_type_select, 'value', lambda x: x == 'Character Universe')
                    
                    with universe_container:
                        universe_type = ui.select(
                            options=[
                                'Royal Family',
                                'Magical Academy',
                                'Adventurer Guild',
                                'Mythical Creatures',
                                'Ancient Gods'
                            ],
                            value='Magical Academy',
                            label='Universe Type'
                        ).classes('w-48')

                    # Alternate Reality specific options
                    reality_container = ui.column().classes('w-full items-center gap-2')
                    reality_container.bind_visibility_from(fantasy_type_select, 'value', lambda x: x == 'Alternate Reality')
                    
                    with reality_container:
                        reality_type = ui.select(
                            options=[
                                'Steampunk',
                                'Cyberpunk',
                                'Post-Apocalyptic',
                                'Utopian',
                                'Magical Realism'
                            ],
                            value='Steampunk',
                            label='Reality Type'
                        ).classes('w-48')

                def update_num_entries(event):
                    global num_entries
                    try:
                        value = event.value
                        if value is None:
                            num_entries = 1
                        else:
                            num_entries = max(1, int(value))
                    except (ValueError, TypeError):
                        num_entries = 1
                        ui.notify('Invalid number, using default value of 1', type='warning')

                ui.number(
                    'Number of Entries',
                    value=1,
                    min=1,
                    max=10,  # Add a reasonable maximum
                    format='%d',  # Force integer format
                    on_change=update_num_entries
                ).classes('w-40')

                with ui.row().classes('gap-4'):
                    ui.button('Generate Data', on_click=lambda: generate_data()).classes('px-4')
                    ui.button('🎲 Surprise Me!', on_click=lambda: generate_surprise()).classes('px-4 bg-purple-600')
                    ui.button('Export', on_click=lambda: export_data(export_format)).classes('px-4')

        with ui.tab_panel('Favorites'):
            global favorites_container
            favorites_container = ui.column().classes('w-full')
            refresh_containers()

        with ui.tab_panel('History'):
            global history_container
            history_container = ui.column().classes('w-full')
            refresh_containers()

        with ui.tab_panel('Settings'):
            with ui.column().classes('w-full gap-4 p-4'):
                def update_export_format(e):
                    global export_format
                    export_format = e.value
                    ui.notify(f'Default export format set to {e.value.upper()}')

                ui.select(
                    ['json', 'csv', 'sql'],
                    value=export_format,
                    label='Default Export Format',
                    on_change=update_export_format
                ).classes('w-48')
                
                def update_max_history(e):
                    global max_history_entries
                    max_history_entries = int(e.value)
                    ui.notify(f'Max history entries set to {max_history_entries}')

                ui.number(
                    'Max History Entries',
                    value=max_history_entries,
                    min=1,
                    max=100,
                    on_change=update_max_history
                ).classes('w-48')

# Move generate_fantasy_data and generate_character_story functions before main_page
def generate_fantasy_data(count=1, fantasy_type='Time Travel', subtype='Medieval', include_story=False):
    try:
        # Build the prompt based on fantasy type
        base_prompt = f"""Generate {count} {'interconnected' if fantasy_type == 'Character Universe' else ''} fantasy characters with rich details.
        
        Fantasy Type: {fantasy_type}
        Sub-type: {subtype}
        
        Requirements:
        - Create {'interconnected' if fantasy_type == 'Character Universe' else 'unique'} characters
        - Include fantasy-specific details
        - Maintain internal consistency
        - {'Include relationships between characters' if fantasy_type == 'Character Universe' else ''}
        
        Return valid JSON with this structure:
        {{
            "people": [
                {{
                    "full_name": "fantasy appropriate name",
                    "title": "character title or role",
                    "age": "age or age range",
                    "origin": "place of origin",
                    "occupation": "fantasy appropriate role",
                    "special_traits": ["trait1", "trait2"],
                    "equipment": ["item1", "item2"],
                    {'\"relationships\": [{{\"to\": \"other_character_name\", \"type\": \"relationship_type"}}],' if fantasy_type == 'Character Universe' else ''}
                    "backstory": "brief character backstory"
                }}
            ]
        }}"""

        if include_story:
            base_prompt += """\nAlso include for each character:
            "daily_life": "description of typical day",
            "notable_events": ["event1", "event2"],
            "future_goals": "character ambitions\""""

        print(f"Generating fantasy data with type: {fantasy_type}, subtype: {subtype}")
        response = model.generate_content(base_prompt)
        return process_response(response)

    except Exception as e:
        print(f"Error generating fantasy data: {str(e)}")
        ui.notify(f'Error: {str(e)}', type='error')
        return None

def generate_character_story(character_data):
    try:
        # Build character info from available data
        story_prompt = f"""Create an engaging short story about this character:
        Name: {character_data.get('full_name', 'Unknown')}
        Occupation: {character_data.get('occupation', 'Unknown')}
        {'Title: ' + character_data['title'] if 'title' in character_data else ''}
        {'Origin: ' + character_data['origin'] if 'origin' in character_data else ''}
        {'Backstory: ' + character_data['backstory'] if 'backstory' in character_data else ''}
        
        Include:
        - A day in their life
        - A significant event
        - Their hopes and dreams
        - Their challenges
        
        Make it engaging and creative while staying true to their background.
        Return the story in this JSON format:
        {{
            "title": "story title",
            "chapters": [
                {{
                    "heading": "chapter name",
                    "content": "chapter text"
                }}
            ],
            "epilogue": "brief conclusion"
        }}"""

        response = model.generate_content(story_prompt)
        
        # Process the response
        response_text = response.text.strip()
        if '```' in response_text:
            response_text = response_text.split('```')[1].strip()
            if response_text.startswith('json'):
                response_text = response_text[4:].strip()
        response_text = response_text.replace('```', '').strip()
        
        story_data = json.loads(response_text)
        
        # Validate story structure
        if not all(key in story_data for key in ['title', 'chapters', 'epilogue']):
            raise ValueError("Invalid story format")
            
        return story_data

    except Exception as e:
        print(f"Error generating story: {str(e)}")
        ui.notify(f'Error generating story: {str(e)}', type='error')
        return {
            "title": "A Simple Tale",
            "chapters": [{
                "heading": "Chapter 1",
                "content": f"A story about {character_data.get('full_name', 'someone special')}..."
            }],
            "epilogue": "To be continued..."
        }

# Function to generate fake data using Gemini API
def generate_fake_data(count=1):
    try:
        # More specific prompt to ensure consistent JSON format
        prompt = f"""Generate exactly {count} different fake persons. Each person must have completely different details.
        Return a JSON object with an array of {count} people.
        
        Requirements:
        - Generate EXACTLY {count} unique people
        - Each person must have different names, emails, addresses, and occupations
        - Return ONLY valid JSON with no additional text
        - Do not include any markdown formatting
        
        Required JSON format:
        {{
            "people": [
                {{
                    "full_name": "(unique full name)",
                    "email": "(unique email)",
                    "address": "(unique address)",
                    "phone_number": "(unique phone)",
                    "occupation": "(unique occupation)"
                }}
                // Repeat for exactly {count} people with different details
            ]
        }}"""
        
        print(f"Sending request to Gemini API for {count} entries...")
        response = model.generate_content(prompt)
        print(f"Received response: {response.text}")
        
        try:
            response_text = response.text.strip()
            
            # Remove any markdown formatting if present
            if '```' in response_text:
                response_text = response_text.split('```')[1]
                if '\n' in response_text:
                    response_text = response_text.split('\n', 1)[1]
            
            response_text = response_text.replace('```', '').strip()
            data = json.loads(response_text)
            
            # Verify we got the requested number of entries
            if isinstance(data, dict) and 'people' in data:
                if len(data['people']) != count:
                    print(f"Warning: Received {len(data['people'])} entries instead of {count}")
                    if len(data['people']) < count:
                        return generate_fake_data(count)
                return data
            elif isinstance(data, list):
                return {"people": data}
            else:
                return {"people": [data]}
                
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            ui.notify(f'Error: Invalid JSON response from API: {str(e)}', type='error')
            return None
            
    except Exception as e:
        print(f"General error: {str(e)}")
        ui.notify(f'Error generating data: {str(e)}', type='error')
        return None

# Function to generate data and display it
async def generate_data():
    ui.notify('Generating data...', type='info')
    try:
        # Get current mode and options
        current_mode = mode.value if mode else 'Regular'
        data = None
        
        if current_mode == 'Regular':
            data = generate_fake_data(count=num_entries)
        elif current_mode == 'Fantasy Mode':
            f_type = fantasy_type_select.value if fantasy_type_select else 'Time Travel'
            subtype = ''
            if f_type == 'Time Travel':
                subtype = era.value if era else 'Medieval (500 - 1500)'
            elif f_type == 'Character Universe':
                subtype = universe_type.value if universe_type else 'Magical Academy'
            elif f_type == 'Alternate Reality':
                subtype = reality_type.value if reality_type else 'Steampunk'
            data = generate_fantasy_data(count=num_entries, fantasy_type=f_type, subtype=subtype)
        elif current_mode == 'Story Mode':
            data = generate_fake_data(count=1)
            if data:
                story = generate_character_story(data['people'][0])
                if story:
                    data['story'] = story

        if data:
            show_data_dialog(data, mode=current_mode)
            add_to_history(data)
        else:
            ui.notify('Failed to generate data', type='error')
    except Exception as e:
        print(f"Error: {str(e)}")
        ui.notify(f'Error: {str(e)}', type='error')

# Function to export data to JSON file
async def export_to_json():
    data = generate_fake_data(count=num_entries)
    if data:
        try:
            with open('fake_data.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)
            ui.notify('Data exported to fake_data.json')
        except Exception as e:
            ui.notify(f'Error exporting data: {str(e)}')
    else:
        ui.notify('No data to export')

# Add this new function for surprise data generation
def generate_surprise_data(count=1):
    try:
        # More creative prompt for surprising results
        prompt = f"""Generate {count} CREATIVE and UNUSUAL (but realistic) fake person(s).
        Return ONLY a valid JSON object with no additional text or formatting.
        Make the data interesting and unique, including:
        - Unusual but real occupations (e.g., "Professional Panda Nanny", "Ethical Hacker")
        - Quirky but valid email addresses
        - Real but uncommon locations
        - Interesting but possible phone numbers

        IMPORTANT: Return EXACTLY this JSON format with no extra text:
        {{
            "people": [
                {{
                    "full_name": "unique name",
                    "email": "valid.email@example.com",
                    "address": "real address format",
                    "phone_number": "valid phone",
                    "occupation": "unusual occupation"
                }}
            ]
        }}

        Make sure:
        1. All JSON is properly formatted with correct commas and brackets
        2. All strings are in double quotes
        3. No trailing commas
        4. No comments or additional text"""
        
        print("Generating surprise data...")
        response = model.generate_content(prompt)
        print(f"Raw response: {response.text}")  # Debug log
        
        # Process the response
        response_text = response.text.strip()
        
        # Remove any markdown formatting
        if '```' in response_text:
            parts = response_text.split('```')
            for part in parts:
                if '{' in part and '}' in part:
                    response_text = part.strip()
                    break
            # Remove any language identifier
            if response_text.startswith('json'):
                response_text = response_text[4:].strip()
        
        # Clean up the JSON string
        response_text = response_text.strip('`').strip()
        print(f"Cleaned JSON string: {response_text}")  # Debug log
        
        # Parse JSON
        data = json.loads(response_text)
        
        # Validate structure
        if not isinstance(data, dict) or 'people' not in data or not isinstance(data['people'], list):
            raise ValueError("Invalid response format")
        
        return data
            
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        print(f"Problematic JSON string: {response_text}")  # Debug log
        ui.notify('Error: Invalid response format. Please try again.', type='error')
        return None
    except Exception as e:
        print(f"Error generating surprise data: {str(e)}")
        ui.notify(f'Error generating surprise data: {str(e)}', type='error')
        return None

# Add this helper function to avoid code duplication
def process_response(response):
    try:
        response_text = response.text.strip()
        
        # Remove any markdown formatting if present
        if '```' in response_text:
            response_text = response_text.split('```')[1]
            if '\n' in response_text:
                response_text = response_text.split('\n', 1)[1]
        
        response_text = response_text.replace('```', '').strip()
        data = json.loads(response_text)
        
        # Ensure the response has the expected structure
        if isinstance(data, dict) and 'people' in data:
            return data
        elif isinstance(data, list):
            return {"people": data}
        else:
            return {"people": [data]}
            
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        ui.notify(f'Error: Invalid JSON response from API: {str(e)}', type='error')
        return None

# Update these functions to use a simpler refresh mechanism
def save_to_favorites(data):
    global saved_favorites
    saved_favorites.extend(data['people'])
    ui.notify('Added to favorites!', type='success')
    refresh_containers()  # Call the new refresh function

def remove_from_favorites(index):
    global saved_favorites
    saved_favorites.pop(index)
    ui.notify('Removed from favorites', type='info')
    refresh_containers()  # Call the new refresh function

def add_to_history(data):
    global generation_history
    generation_history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'data': data
    })
    if len(generation_history) > max_history_entries:
        generation_history.pop(0)
    refresh_containers()  # Call the new refresh function

def clear_history():
    global generation_history
    generation_history.clear()
    ui.notify('History cleared', type='info')
    refresh_containers()  # Call the new refresh function

# Add this new function to refresh both containers
def refresh_containers():
    if favorites_container:
        favorites_container.clear()
        with favorites_container:
            with ui.scroll_area().classes('w-full h-96'):
                with ui.column().classes('w-full gap-4 p-4'):
                    if not saved_favorites:
                        ui.label('No favorites yet').classes('text-center text-gray-500')
                    for i, person in enumerate(saved_favorites):
                        with ui.card().classes('w-full'):
                            with ui.row().classes('w-full justify-between items-center'):
                                ui.label(f"Person {i+1}").classes('text-h6')
                                ui.button(icon='delete', on_click=lambda i=i: remove_from_favorites(i))
                            for key, value in person.items():
                                ui.label(f"{key.replace('_', ' ').title()}: {value}")

    if history_container:
        history_container.clear()
        with history_container:
            with ui.scroll_area().classes('w-full h-96'):
                with ui.column().classes('w-full gap-4 p-4'):
                    ui.button('Clear History', on_click=clear_history).classes('self-end')
                    if not generation_history:
                        ui.label('No history yet').classes('text-center text-gray-500')
                    for entry in reversed(generation_history):
                        with ui.card().classes('w-full'):
                            ui.label(f"Generated on: {entry['timestamp']}").classes('text-h6')
                            for person in entry['data']['people']:
                                ui.label(f"Name: {person['full_name']}")
                            ui.separator()

async def export_data(format_type='json'):
    data = generate_fake_data(count=num_entries)
    if data:
        try:
            filename = f'fake_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
            if format_type == 'json':
                with open(f'{filename}.json', 'w') as f:
                    json.dump(data, f, indent=4)
            elif format_type == 'csv':
                with open(f'{filename}.csv', 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=data['people'][0].keys())
                    writer.writeheader()
                    writer.writerows(data['people'])
            elif format_type == 'sql':
                with open(f'{filename}.sql', 'w') as f:
                    f.write("CREATE TABLE IF NOT EXISTS people (\n")
                    f.write("    id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
                    f.write("    full_name TEXT,\n")
                    f.write("    email TEXT,\n")
                    f.write("    address TEXT,\n")
                    f.write("    phone_number TEXT,\n")
                    f.write("    occupation TEXT\n")
                    f.write(");\n\n")
                    
                    f.write("INSERT INTO people (full_name, email, address, phone_number, occupation) VALUES\n")
                    values = []
                    for person in data['people']:
                        values.append(f"('{person['full_name']}', '{person['email']}', '{person['address']}', '{person['phone_number']}', '{person['occupation']}')")
                    f.write(",\n".join(values) + ";")
            ui.notify(f'Data exported as {format_type.upper()} to {filename}.{format_type}', type='success')
        except Exception as e:
            ui.notify(f'Error exporting data: {str(e)}', type='error')

# Add the missing generate_surprise function
async def generate_surprise():
    ui.notify('Generating surprising data...', type='info')
    try:
        data = generate_surprise_data(count=num_entries)
        if data and data.get('people'):
            with ui.dialog() as dialog, ui.card().classes('w-96 dialog-content'):
                # Add header with title and favorite button
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.label('🎲 Surprise Data Generated!').classes('text-h6')
                    ui.button(icon='favorite', on_click=lambda: save_to_favorites(data)).classes(
                        'text-red-500 bg-transparent hover:bg-red-50'
                    ).tooltip('Add to Favorites')

                with ui.column().classes('max-h-96 overflow-auto'):
                    for i, person in enumerate(data.get('people', [])):
                        ui.label(f"Person {i+1}:").classes('text-h6 mt-4')
                        ui.label(f"Name: {person.get('full_name')}").classes('mt-2')
                        ui.label(f"Email: {person.get('email')}").classes('mt-2')
                        ui.label(f"Address: {person.get('address')}").classes('mt-2')
                        ui.label(f"Phone: {person.get('phone_number')}").classes('mt-2')
                        ui.label(f"Occupation: {person.get('occupation')}").classes('mt-2')
                        if i < len(data.get('people')) - 1:
                            ui.separator().classes('my-4')
                
                # Footer with close button
                with ui.row().classes('w-full justify-between mt-4'):
                    ui.button('Close', on_click=dialog.close)
                    ui.button(
                        'Add to Favorites', 
                        on_click=lambda: [save_to_favorites(data), dialog.close()]
                    ).classes('bg-red-600')
                dialog.open()
                # Add to history after showing dialog
                add_to_history(data)
        else:
            ui.notify('Failed to generate surprise data', type='error')
    except Exception as e:
        print(f"Error in generate_surprise: {str(e)}")
        ui.notify(f'Error: {str(e)}', type='error')

# Make sure these are at the very end of the file
ui.page('/')(main_page)
ui.run(reload=False)  # Add reload=False to prevent auto-reload issues
