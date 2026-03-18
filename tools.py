import subprocess
import os
from logger import get_logger

logger = get_logger("tools")

def run_command(cmd: str) -> str:
    """Executes a bash command and returns the output."""
    try:
        logger.info(f"Executing command: {cmd}")
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        if result.returncode != 0:
            logger.error(f"Command failed with return code {result.returncode}: {error}")
            return f"ERROR: {error}"
            
        return output if output else "Command executed successfully (no output)."
    except Exception as e:
        logger.error(f"Exception during command execution: {str(e)}")
        return f"EXCEPTION: {str(e)}"

def read_file(path: str) -> str:
    """Reads content from a file."""
    try:
        if not os.path.exists(path):
            return "ERROR: File not found."
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {str(e)}"

def write_file(path: str, content: str) -> str:
    """Writes content to a file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File written successfully to {path}"
    except Exception as e:
        return f"ERROR: {str(e)}"
