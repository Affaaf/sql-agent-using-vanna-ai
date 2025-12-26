import os

from utils.prompt_builder import EcommerceSystemPromptBuilder
from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.tools import VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool, SaveTextMemoryTool
from vanna.servers.fastapi import VannaFastAPIServer
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.openai import OpenAILlmService
from dotenv import load_dotenv
from utils.db_agent import create_db_tool
from constants.constant import Const

load_dotenv()


llm = OpenAILlmService(

    api_key=os.getenv("OPENAI_API_KEY"),
    model=Const.LLM,
)

# Configure your agent memory
agent_memory = DemoAgentMemory(max_items=1000)

# Configure user authentication
class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        user_email = request_context.get_cookie('vanna_email') or 'guest@example.com'
        group = 'admin' if user_email == 'admin@example.com' else 'user'
        return User(id=user_email, email=user_email, group_memberships=[group])

user_resolver = SimpleUserResolver()

# Create your agent
tools = ToolRegistry()
# tools.register_local_tool(db_tool, access_groups=['admin', 'user'])
tools.register_local_tool(create_db_tool(), access_groups=['admin', 'user'])

tools.register_local_tool(SaveQuestionToolArgsTool(), access_groups=['admin'])
tools.register_local_tool(SearchSavedCorrectToolUsesTool(), access_groups=['admin', 'user'])
tools.register_local_tool(SaveTextMemoryTool(), access_groups=['admin', 'user'])
tools.register_local_tool(VisualizeDataTool(), access_groups=['admin', 'user'])

agent = Agent(
    llm_service=llm,
    tool_registry=tools,
    user_resolver=user_resolver,
    agent_memory=agent_memory,
    system_prompt_builder=EcommerceSystemPromptBuilder()

)

# Run the server
server = VannaFastAPIServer(agent)
server.run()
