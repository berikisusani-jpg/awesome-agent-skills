import os
import datetime

class RecursiveModificationProtocol:
    def __init__(self, brain):
        self.brain = brain
        self.review_dir = "core_review"
        if not os.path.exists(self.review_dir):
            os.makedirs(self.review_dir)

    async def propose_core_improvement(self, target_file):
        """
        Analyzes a core module and proposes improvements via a diff file.
        Requires manual human review before application.
        """
        if not os.path.exists(target_file):
            return f"Error: {target_file} not found."

        with open(target_file, "r") as f:
            original_code = f.read()

        prompt = f"""
        Analyze the following Project FRIDAY core module:
        ---
        FILE: {target_file}
        CODE:
        {original_code}
        ---
        Suggest performance optimizations or code quality improvements.
        Output ONLY the improved code, no explanations.
        """

        improved_code = ""
        async for chunk in self.brain.chat_stream(prompt):
            improved_code += chunk

        # Generate a diff-like review file instead of overwriting
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        review_filename = f"{os.path.basename(target_file)}_{timestamp}.review"
        review_path = os.path.join(self.review_dir, review_filename)

        with open(review_path, "w") as f:
            f.write(f"PROPOSED CHANGES FOR: {target_file}\n")
            f.write("="*40 + "\n")
            f.write(improved_code)

        print(f"Friday: Proposed improvements for {target_file} saved to {review_path}")
        return f"Improvement proposal generated at {review_path}. Manual review required."
