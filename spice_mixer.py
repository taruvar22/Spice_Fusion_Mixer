import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import get_cmap
import warnings
warnings.filterwarnings('ignore')

def load_spice_data():
    """Load spice data from CSV file"""
    try:
        df = pd.read_csv('spice_flavor_profile.csv')
        return df
    except Exception as e:
        print(f"Error loading spice data: {e}")
        print("\nTroubleshooting Tips:")
        print("1. Ensure 'spice_flavor_profile.csv' is in the same folder")
        print("2. Verify CSV has columns: Spice Name, Sweetness, Sourness, Saltiness, Spiciness, Bitterness, Umami")
        print("3. Install required packages: pandas, matplotlib (pip install pandas matplotlib)")
        return None

def select_spices(df):
    """Let user select spices from the dataset"""
    print("\nAvailable Spices:")
    for i, spice in enumerate(df['Spice Name'], 1):
        print(f"{i}. {spice}")
    
    selected = []
    while True:
        try:
            choice = input("\nEnter spice number (or 'done' to finish): ")
            if choice.lower() == 'done':
                break
            index = int(choice) - 1
            if 0 <= index < len(df):
                selected.append(index)
                print(f"Added: {df.iloc[index]['Spice Name']}")
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a number or 'done'")
    
    return selected

def calculate_blend(df, selected_indices):
    """Calculate the average flavor profile of selected spices"""
    if not selected_indices:
        return None
    
    selected_spices = df.iloc[selected_indices]
    averages = selected_spices.mean(numeric_only=True)
    
    return {
        "Spices Used": list(selected_spices['Spice Name']),
        "Flavor Profile": {
            "Sweetness": round(averages['Sweetness'], 1),
            "Sourness": round(averages['Sourness'], 1),
            "Saltiness": round(averages['Saltiness'], 1),
            "Spiciness": round(averages['Spiciness'], 1),
            "Bitterness": round(averages['Bitterness'], 1),
            "Umami": round(averages['Umami'], 1)
        }
    }

def plot_flavor_profile(flavor_profile):
    """Generate perfectly aligned vertical bar chart"""
    # Sort by value while preserving flavor names
    flavors, values = zip(*sorted(flavor_profile.items(), 
                                key=lambda item: item[1], 
                                reverse=True))
    
    # Create figure with constrained layout
    fig, ax = plt.subplots(figsize=(10, 6), 
                        layout='constrained')
    
    # Create bars with consistent width
    bars = ax.bar(flavors, values, 
                 width=0.6,
                 color=get_cmap('plasma')(np.linspace(0.2, 0.8, len(flavors))))
    
    # Add centered value labels above bars
    ax.bar_label(bars, 
                padding=3,
                labels=[f'{v}%' for v in values],
                fontsize=10,
                color='black')
    
    # Formatting
    ax.set_ylim(0, 100)
    ax.set_ylabel('Intensity (%)', fontsize=12)
    ax.set_title('Spice Blend Flavor Profile', 
                fontsize=16, 
                pad=20)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    
    # Rotate x-labels for readability
    plt.xticks(rotation=45, ha='right')
    plt.show()

def display_results(result):
    """Display results with perfect-alignment visualization"""
    if not result:
        print("No spices selected!")
        return
    
    print("\n\n=== SPICE FUSION RESULTS ===")
    print(f"\nSpices Used: {', '.join(result['Spices Used'])}")
    
    print("\nFinal Flavor Profile (%):")
    for flavor, value in result['Flavor Profile'].items():
        print(f"{flavor:10}: {value}%")
    
    dominant = max(result['Flavor Profile'].items(), key=lambda x: x[1])
    print(f"\nDominant Flavor: {dominant[0]} ({dominant[1]}%)")
    
    # Generate visualization
    try:
        plot_flavor_profile(result['Flavor Profile'])
    except Exception as e:
        print(f"\n[Note] Visualization skipped (Error: {e})")

def main():
    print("""
   _____       _       ______                 _   _             
  / ____|     (_)     |  ____|               | | (_)            
 | (___  _ __  _ ___  | |__ _   _ _ __   ___| |_ _  ___  _ __  
  \___ \| '_ \| / __| |  __| | | | '_ \ / __| __| |/ _ \| '_ \ 
  ____) | |_) | \__ \ | |  | |_| | | | | (__| |_| | (_) | | | |
 |_____/| .__/|_|___/ |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|
        | |                                                     
        |_|          Spice Fusion Mixer v2.2
    """)
    
    df = load_spice_data()
    if df is None:
        return
    
    selected = select_spices(df)
    blend = calculate_blend(df, selected)
    display_results(blend)
    
    # Optional save feature
    save = input("\nWould you like to save this blend? (y/n): ").lower()
    if save == 'y':
        blend_name = input("Name your blend: ")
        with open('my_spice_blends.txt', 'a') as f:
            f.write(f"\n{blend_name}: {', '.join(blend['Spices Used'])}\n")
            for flavor, value in blend['Flavor Profile'].items():
                f.write(f"{flavor}: {value}%\n")
        print("Blend saved to 'my_spice_blends.txt'")

if __name__ == "__main__":
    main()