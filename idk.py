import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_relay_diagram():
    fig, ax = plt.subplots(figsize=(12, 8))

    # Draw relay
    ax.add_patch(patches.Rectangle((1, 5), 3, 4, edgecolor="black", facecolor="lightgrey", label="Relay"))
    ax.text(2.5, 9.2, "TWTADE YJ2N-12VDC Relay", ha="center", fontsize=12, weight="bold")

    # Label pins
    ax.text(0.8, 8, "Pin 8 (+12V)", fontsize=10, va="center")
    ax.text(0.8, 7, "Pin 7 (GND)", fontsize=10, va="center")
    ax.text(0.8, 6, "Pin 5 (COM)", fontsize=10, va="center")
    ax.text(0.8, 5.5, "Pin 6 (NO)", fontsize=10, va="center")

    # Connections to GPIO and power
    ax.arrow(1.5, 8, -1.0, 0, head_width=0.2, head_length=0.3, fc='black', ec='black')
    ax.text(0.2, 8.2, "+12V from Power Supply", fontsize=10, color="blue", va="center")
    ax.arrow(1.5, 7, -1.0, -0.5, head_width=0.2, head_length=0.3, fc='black', ec='black')
    ax.text(0.2, 6.3, "GND to Transistor", fontsize=10, color="blue", va="center")

    # Transistor
    ax.add_patch(patches.Circle((4.5, 5), 0.2, edgecolor="black", facecolor="lightgrey"))
    ax.text(4.5, 5.5, "NPN Transistor", fontsize=10, ha="center")

    # Connections to transistor
    ax.arrow(4.7, 5.2, 1.0, 0.5, head_width=0.2, head_length=0.3, fc='black', ec='black')
    ax.text(6, 5.7, "Base to GPIO (via 1kΩ resistor)", fontsize=10, va="center", color="green")
    ax.arrow(4.3, 4.8, -1.5, -1.0, head_width=0.2, head_length=0.3, fc='black', ec='black')
    ax.text(2.5, 3.5, "Collector to Pin 7", fontsize=10, va="center")
    ax.arrow(4.5, 4.5, 0, -1.5, head_width=0.2, head_length=0.3, fc='black', ec='black')
    ax.text(4.8, 2.5, "Emitter to GND", fontsize=10, color="blue", va="center")

    # Connections to AC Load (Pump)
    ax.arrow(2.5, 6, 1.0, 1.0, head_width=0.2, head_length=0.3, fc='black', ec='black')
    ax.text(4, 7.5, "Live wire to COM", fontsize=10, color="red", va="center")
    ax.arrow(2.5, 5.5, 1.0, -1.0, head_width=0.2, head_length=0.3, fc='black', ec='black')
    ax.text(4, 4.5, "NO to Pump Live", fontsize=10, color="red", va="center")
    ax.text(2, 3, "Neutral and Ground wires go directly to the Pump", fontsize=10, color="black")

    # Diagram aesthetics
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 10)
    ax.axis('off')
    plt.show()

draw_relay_diagram()
