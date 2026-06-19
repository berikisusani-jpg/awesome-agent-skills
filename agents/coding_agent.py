class CodingAgent:
    def write_code(self, prompt):
        print(f"Writing code for: {prompt}")
        return "def hello_world():\n    print('Hello from Friday!')"

    def debug_code(self, code):
        print("Debugging code...")
        return "Code looks clean."
