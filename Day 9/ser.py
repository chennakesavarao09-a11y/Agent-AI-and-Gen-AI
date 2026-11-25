from fastmcp import FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Text

mcp = FastMCP("Student App")

@mcp.tool(app=True)
def student_app():
    with Column(gap=3) as view:
        Heading("My Student Dashboard")
        Text("Welcome to Python and AI!")
        Heading("Total Students: 65")
        Text("Course: Generative AI")

    return PrefabApp(view=view)

if __name__ == "__main__":
    mcp.run()