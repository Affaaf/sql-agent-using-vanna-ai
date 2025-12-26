from vanna.core.system_prompt import SystemPromptBuilder
from vanna.core.user import User
from constants.constant import Const


class EcommerceSystemPromptBuilder(SystemPromptBuilder):

    async def build_system_prompt(
        self,
        user: User,
        tool_schemas,
        context=None
    ) -> str:

        prompt=Const.PROMPT
        prompt += "\n\nAVAILABLE TOOLS:\n"

        for tool in tool_schemas:
            prompt += f"\nTool: {tool.name}\n"
            prompt += f"Description: {tool.description}\n"
            prompt += f"Parameters: {tool.parameters}\n"

        prompt += f"""
        CURRENT USER:
        Email: {user.email}
        Groups: {', '.join(user.group_memberships)}
        """

        return prompt
