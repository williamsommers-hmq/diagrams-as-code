from diagrams import Diagram

from hivemq_theme import HIVEMQ_YELLOW, HiveMQPalette

palette = HiveMQPalette("icons.yaml")
diag_name = "Baltimore_UNS_Standard"
img_file = f"{diag_name}.svg"

with Diagram(diag_name, show=False, outformat="svg", filename=diag_name):
    # Your logic here
    edge = palette.get_node("edge", "Maryland Plant")
    # ...

palette.generate_readme(diag_name, img_file)

print("Diagram generation complete!")
print(f"Generated: {img_file}")
print(f"Generated README.md")
print("")
print("Note: Git and S3 upload functionality is commented out for security reasons.")
print("To enable these features, you would need to:")
print("1. Configure Git credentials")
print("2. Configure AWS credentials")
print("3. Uncomment the push_to_github() and upload_to_s3() lines")
