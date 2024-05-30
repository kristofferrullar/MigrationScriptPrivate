import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define the steps in the business process
steps = [
    ("Start", "User initiates migration"),
    ("LoadConfig", "Load Configuration\n(Functions: load_config)"),
    ("AuthSource", "Authenticate to Source Dataverse\n(Functions: get_access_token)"),
    ("AuthTarget", "Authenticate to Target Dataverse\n(Functions: get_access_token)"),
    ("ReadFetchXML", "Read FetchXML Queries\n(Functions: load_fetchxml_queries, read_fetchxml)"),
    ("ExtractData", "Extract Data from Source\n(Functions: execute_fetchxml_query, extract_entity_name, pluralize_entity_name)"),
    ("TransformData", "Transform Data\n(Functions: transform_data, transform_for_dynamics365, transform_for_other_db)"),
    ("InspectData", "Inspect Transformed Data\n(Functions: inspect_temp_data)"),
    ("LoadData", "Load Data to Target\n(Functions: load_data_to_target)"),
    ("CompleteMigration", "Complete Migration Process\n(Confirmation provided)")
]

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 10))  # Adjusted the figure size to be taller

# Define adjusted box properties for taller boxes
box_props = dict(boxstyle="round,pad=0.5", edgecolor="black", facecolor="lightblue")

# Adjust positions to fit within the width
positions = {
    "Start": (0, 0),
    "LoadConfig": (1, 0),
    "AuthSource": (2, 0),
    "AuthTarget": (3, 0),
    "ReadFetchXML": (4, 0),
    "ExtractData": (5, 0),
    "TransformData": (6, 0),
    "InspectData": (7, 0),
    "LoadData": (8, 0),
    "CompleteMigration": (9, 0)
}

# Draw the steps with adjusted box properties
for step, text in steps:
    x, y = positions[step]
    ax.text(x, y, text, bbox=box_props, ha="center", va="center", fontsize=10)

# Draw arrows between the steps with adjusted positions
for i in range(len(steps) - 1):
    start_step = steps[i][0]
    end_step = steps[i + 1][0]
    start_pos = positions[start_step]
    end_pos = positions[end_step]
    ax.annotate("", xy=end_pos, xytext=start_pos, arrowprops=dict(facecolor="black", arrowstyle='->'))

# Set limits and remove axes
ax.set_xlim(-1, 10)
ax.set_ylim(-1, 1)
ax.axis("off")

# Add a title
plt.title("Business Process Flow Chart for Migration Process")
plt.show()
