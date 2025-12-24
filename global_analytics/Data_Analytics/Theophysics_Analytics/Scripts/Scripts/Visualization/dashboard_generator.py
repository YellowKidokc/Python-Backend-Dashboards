# dashboard_generator.py

import pandas as pd
import plotly.express as px
import os

# --- Configuration ---
# Input data file
THEORY_DATA_FILE = r"D:\THEOPHYSICS_MASTER\00_VAULT_SYSTEM\Scripts\Data\Source\MASTER_THEORY_REFERENCE_SHEET.csv"

# Output directory for charts
CHART_OUTPUT_DIR = r"D:\THEOPHYSICS_MASTER\00_VAULT_SYSTEM\Global_Analytics\Dashboards\charts"

# Dashboard files to update
DASHBOARD_DIR = r"D:\THEOPHYSICS_MASTER\00_VAULT_SYSTEM\Global_Analytics\Dashboards"
ANALYSIS_DASHBOARD = os.path.join(DASHBOARD_DIR, "Analysis_Dashboard.md")

# --- Functions ---

def generate_theories_per_domain_chart(df):
    """Generates a bar chart of theories per domain."""
    print("Generating chart: Theories per Domain")
    domain_counts = df['Domain'].value_counts().reset_index()
    domain_counts.columns = ['Domain', 'Count']
    
    fig = px.bar(domain_counts, 
                 x='Domain', 
                 y='Count', 
                 title='Number of Theories per Domain',
                 labels={'Count': 'Number of Theories', 'Domain': 'Domain'},
                 template='plotly_white')
    fig.update_layout(title_x=0.5)
    
    output_path = os.path.join(CHART_OUTPUT_DIR, "theories_per_domain.html")
    fig.write_html(output_path, include_plotlyjs='cdn')
    return output_path

def generate_theories_per_paper_chart(df):
    """Generates a bar chart of theories per paper."""
    print("Generating chart: Theories per Paper")
    paper_counts = df['Paper_Number'].value_counts().reset_index()
    paper_counts.columns = ['Paper_Number', 'Count']
    
    fig = px.bar(paper_counts,
                 x='Paper_Number',
                 y='Count',
                 title='Number of Theories per Paper',
                 labels={'Count': 'Number of Theories', 'Paper_Number': 'Paper Number'},
                 template='plotly_white')
    fig.update_layout(title_x=0.5)

    output_path = os.path.join(CHART_OUTPUT_DIR, "theories_per_paper.html")
    fig.write_html(output_path, include_plotlyjs='cdn')
    return output_path

def generate_theory_type_distribution_chart(df):
    """Generates a pie chart of the theory type distribution."""
    print("Generating chart: Theory Type Distribution")
    type_counts = df['Theory_Type'].value_counts().reset_index()
    type_counts.columns = ['Theory_Type', 'Count']

    fig = px.pie(type_counts,
                 names='Theory_Type',
                 values='Count',
                 title='Distribution of Theory Types',
                 template='plotly_white')
    fig.update_layout(title_x=0.5)

    output_path = os.path.join(CHART_OUTPUT_DIR, "theory_type_distribution.html")
    fig.write_html(output_path, include_plotlyjs='cdn')
    return output_path
    
def inject_chart_into_dashboard(dashboard_file, chart_html_path, section_title):
    """Injects an HTML chart into a markdown dashboard file."""
    chart_filename = os.path.basename(chart_html_path)
    iframe_tag = f'<iframe src="charts/{chart_filename}" width="100%" height="500px" frameborder="0"></iframe>'
    
    print(f"Injecting chart '{chart_filename}' into '{os.path.basename(dashboard_file)}'")
    
    with open(dashboard_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Simple replacement for now, can be made more robust
    if section_title in content:
        # This is a placeholder for more robust injection logic
        # For now, we will just append it.
        pass
        
    # Append the chart at the end for this first version
    content += f"\n\n## {section_title}\n{iframe_tag}\n"
    
    with open(dashboard_file, "w", encoding="utf-8") as f:
        f.write(content)


# --- Main Execution ---

def main():
    """Main function to generate and inject charts."""
    print("Starting dashboard generator...")
    
    # Ensure output directory exists
    if not os.path.exists(CHART_OUTPUT_DIR):
        print(f"Creating directory: {CHART_OUTPUT_DIR}")
        os.makedirs(CHART_OUTPUT_DIR)
        
    # Load the data
    try:
        print(f"Loading data from: {THEORY_DATA_FILE}")
        df = pd.read_csv(THEORY_DATA_FILE)
    except FileNotFoundError:
        print(f"ERROR: Data file not found at {THEORY_DATA_FILE}. Cannot proceed.")
        return

    # Generate charts
    domain_chart_path = generate_theories_per_domain_chart(df)
    paper_chart_path = generate_theories_per_paper_chart(df)
    type_chart_path = generate_theory_type_distribution_chart(df)
    
    # Inject charts into the main analysis dashboard
    # For this initial version, we will just inject into one dashboard.
    if os.path.exists(ANALYSIS_DASHBOARD):
        inject_chart_into_dashboard(ANALYSIS_DASHBOARD, domain_chart_path, "Theories per Domain")
        inject_chart_into_dashboard(ANALYSIS_DASHBOARD, paper_chart_path, "Theories per Paper")
        inject_chart_into_dashboard(ANALYSIS_DASHBOARD, type_chart_path, "Theory Type Distribution")
    else:
        print(f"WARNING: Dashboard file not found at {ANALYSIS_DASHBOARD}. Cannot inject charts.")

    print("Dashboard generator finished successfully.")

if __name__ == "__main__":
    main()
