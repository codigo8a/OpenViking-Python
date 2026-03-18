import os
from logger import get_logger

logger = get_logger("skills")

class SkillsManager:
    def __init__(self, skills_dir="skills"):
        self.skills_dir = skills_dir
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)
            
    def get_available_skills(self):
        """Lists help strings for all found skills."""
        skills = []
        for file in os.listdir(self.skills_dir):
            if file.endswith(".py") and not file.startswith("__"):
                path = os.path.join(self.skills_dir, file)
                desc = self._extract_description(path)
                skills.append({
                    "name": file.replace(".py", ""),
                    "description": desc,
                    "usage": f"python {path} [args]"
                })
        return skills

    def _extract_description(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if first_line.startswith("#"):
                    return first_line.replace("#", "").strip()
            return "No description available."
        except:
            return "Error reading description."

skills_manager = SkillsManager()
