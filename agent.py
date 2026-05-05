import asyncio
import json
from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_core.tools import StructuredTool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field, create_model

# === Connexion aux serveurs MCP ===
async def get_mcp_tools_async(url: str):
    tools = []
    async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            for tool in result.tools:
                tool_name = tool.name
                tool_desc = tool.description
                input_schema = tool.inputSchema

                fields = {}
                properties = input_schema.get("properties", {})
                required = input_schema.get("required", [])
                for prop_name, prop_info in properties.items():
                    prop_type = prop_info.get("type", "string")
                    if prop_type == "integer":
                        py_type = int
                    elif prop_type == "number":
                        py_type = float
                    else:
                        py_type = str
                    if prop_name in required:
                        fields[prop_name] = (py_type, Field(description=prop_info.get("description", "")))
                    else:
                        fields[prop_name] = (py_type, Field(default=None, description=prop_info.get("description", "")))

                DynamicModel = create_model(f"{tool_name}_input", **fields)

                async def call_tool_async(url=url, name=tool_name, **kwargs):
                    async with sse_client(url) as (r, w):
                        async with ClientSession(r, w) as s:
                            await s.initialize()
                            res = await s.call_tool(name, kwargs)
                            return str(res.content[0].text)

                def make_sync(async_fn, u=url, n=tool_name):
                    def sync_fn(**kwargs):
                        return asyncio.run(async_fn(url=u, name=n, **kwargs))
                    return sync_fn

                tools.append(StructuredTool(
                    name=tool_name,
                    description=tool_desc,
                    args_schema=DynamicModel,
                    func=make_sync(call_tool_async, u=url, n=tool_name)
                ))
    return tools

def get_all_tools():
    servers = [
        "http://localhost:3333/sse",
        "http://localhost:3334/sse",
        "http://localhost:3335/sse",
        "http://localhost:3336/sse",
        "http://localhost:3337/sse",
    ]
    all_tools = []
    for url in servers:
        try:
            tools = asyncio.run(get_mcp_tools_async(url))
            all_tools.extend(tools)
            print(f"✅ Connecté à {url} — {len(tools)} outil(s)")
        except Exception as e:
            print(f"❌ Erreur connexion {url}: {e}")
    return all_tools

tools = get_all_tools()
llm = ChatGroq(model="llama-3.3-70b-versatile")
agent_executor = create_react_agent(llm, tools)

# === Exercice 1 : retourne aussi les étapes ===
def run_travel_agent_with_steps(user_request: str):
    steps = []
    response = agent_executor.invoke({
        "messages": [{"role": "user", "content": user_request}]
    })

    # Extraire les appels d'outils depuis les messages
    for message in response["messages"]:
        # Messages d'appel d'outil
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tc in message.tool_calls:
                steps.append({
                    "tool": tc["name"],
                    "args": tc["args"],
                    "result": ""
                })
        # Messages de résultat d'outil
        if hasattr(message, "name") and message.name:
            for step in reversed(steps):
                if step["tool"] == message.name and step["result"] == "":
                    step["result"] = message.content
                    break

    final_output = response["messages"][-1].content
    return final_output, steps

# === Fonction simple (gardée pour compatibilité) ===
def run_travel_agent(user_request: str):
    final_output, _ = run_travel_agent_with_steps(user_request)
    return final_output

# === Exercice 2 : Agent critique ===
critic_llm = ChatGroq(model="llama-3.3-70b-versatile")

def critic_agent(travel_plan: str) -> str:
    """Valide et critique le plan de voyage généré."""
    response = critic_llm.invoke([
        {
            "role": "system",
            "content": """Tu es un agent critique expert en voyages.
Tu reçois un plan de voyage et tu dois :
1. Vérifier que le budget est réaliste
2. Vérifier que les activités sont cohérentes avec la météo
3. Identifier les points manquants ou améliorables
4. Donner une note sur 10
Sois concis et constructif."""
        },
        {
            "role": "user",
            "content": f"Voici le plan de voyage à évaluer :\n\n{travel_plan}"
        }
    ])
    return response.content