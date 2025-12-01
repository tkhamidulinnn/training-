import os
import csv
import json
import click  # INSTALLATION: pip install click

# ==========================================
# ⚙️ EXPORT CONFIGURATION
# ==========================================
DEFAULT_OUTPUT_DIR = os.getenv("EXPORT_DIR", "./exports")
MAX_ROWS = int(os.getenv("MAX_EXPORT_ROWS", "1000"))

@click.command()
@click.option('--format', type=click.Choice(['csv', 'json']), default='csv', help='Output format')
@click.option('--filename', default='data_export', help='Output filename (without extension)')
def export_data(format, filename):
    """
    CLI Tool to export database records to local files.
    
    Usage:
        python export_tool.py --format json --filename my_report
    """
    
    # Ensure directory exists
    if not os.path.exists(DEFAULT_OUTPUT_DIR):
        os.makedirs(DEFAULT_OUTPUT_DIR)
        
    file_path = os.path.join(DEFAULT_OUTPUT_DIR, f"{filename}.{format}")
    
    print(f"Starting export to {file_path}...")
    print(f"Configuration: Max Rows = {MAX_ROWS}")

    # Dummy Data
    data = [
        {"id": 1, "name": "Alice", "role": "Admin"},
        {"id": 2, "name": "Bob", "role": "User"}
    ]

    try:
        if format == 'json':
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            with open(file_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                
        click.echo(click.style(f"✅ Success! Data exported to {file_path}", fg='green'))
        
    except Exception as e:
        click.echo(click.style(f"❌ Error: {e}", fg='red'))

if __name__ == '__main__':
    export_data()
