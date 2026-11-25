from fastmcp import FastMCP
from google import genai

mcp=FastMCP("Gemini Calculator")

client=genai.Client(api_key="")
@mcp.tool()
def ask_gemini(questions:str):
    response=client.models.generate_content(
        model="gemini-3.5-flash",
        contents=questions
    )
    return response.text

@mcp.tool()
def calculator(a:float,b:float,opertion:str):
    if opertion=="add":
        return a+b
    if opertion=="sub":
        return a-b
    
if __name__=="__main__":
    mcp.run()