import re
from llm_router import router
from tools import run_command
from memory import memory
from planner import planner
from skills_manager import skills_manager
from mcp_manager import mcp_manager
import asyncio
from logger import get_logger

logger = get_logger("agent")

class OpenVikingAgent:
    def __init__(self):
        self.running = True

    def parse_response(self, text: str):
        """Parses the LLM structured output."""
        action_match = re.search(r"ACTION:\s*(run_command|answer)", text, re.IGNORECASE)
        command_match = re.search(r"COMMAND:\s*(.*)", text, re.IGNORECASE)
        response_match = re.search(r"RESPONSE:\s*([\s\S]*)", text, re.IGNORECASE)

        action = action_match.group(1).strip() if action_match else "answer"
        command = command_match.group(1).strip() if command_match else ""
        response = response_match.group(1).strip() if response_match else text

        return action, command, response

    def execute_task(self, task: str):
        logger.info(f"New task received: {task}")
        
        # 1. Search memory for context
        context = memory.search_memory(task)
        
        # 2. Get available Skills and MCP Tools
        skills = skills_manager.get_available_skills()
        mcp_tools = []
        try:
            # We use a simple fetch since we can't do full async easily here without changing the whole loop
            mcp_tools = asyncio.run(mcp_manager.list_tools())
        except:
            pass

        # 3. Generate prompt and ask LLM
        prompt = planner.generate_prompt(task, context, skills, mcp_tools)
        llm_output = router.ask(prompt)
        
        # 4. Parse decision
        action, command, response = self.parse_response(llm_output)
        
        logger.info(f"Decision: {action} | Msg: {response}")
        
        final_result = response
        
        # 4. Execute action
        if action == "run_command" and command:
            cmd_output = run_command(command)
            final_result = f"{response}\n\n--- OUTPUT ---\n{cmd_output}"
            
            # Save to memory
            memory.save_memory(f"Task: {task} | Command: {command} | Output: {cmd_output}")
        else:
            memory.save_memory(f"Task: {task} | Response: {response}")

        return final_result

    def run_cli(self):
        print("--- OpenViking CLI (Linux Agent) ---")
        print("Escribe 'exit' para salir.")
        while self.running:
            try:
                task = input("\ntask> ")
                if task.lower() in ["exit", "quit"]:
                    break
                
                result = self.execute_task(task)
                print(f"\n[OpenViking]:\n{result}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Critical error in loop: {e}")
                print(f"Error: {e}")

if __name__ == "__main__":
    agent = OpenVikingAgent()
    agent.run_cli()
