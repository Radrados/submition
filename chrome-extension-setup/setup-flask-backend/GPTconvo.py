import requests
import sqlite3
DEBUG_MODE = True
def debugprint(*args):
    if DEBUG_MODE:
        print(*args)

class GPT3Chatbot:
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = 'https://api.openai.com/v1/chat/completions'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        self.keyword = 'Query-GPT-2C692'
        self.keyword2 = 'databaseoutput'
        self.messages = []  # Initialized as empty, will be set by set_initial_prompt

    def set_initial_prompt(self, prompt):
        self.messages = [{'role': 'system', 'content': prompt}]

    def chat(self, user_input):
        # Append the user's message to the conversation history
        self.messages.append({'role': 'user', 'content': user_input})

        # Make the API request
        response = requests.post(self.endpoint, headers=self.headers, json={"messages": self.messages, "model": "gpt-4"})
        
        if response.status_code == 200:
            assistant_reply = response.json()['choices'][0]['message']['content']

            # Check if the response is an SQL query
            if assistant_reply.startswith(self.keyword) or assistant_reply.startswith(self.keyword2):
                results = self.run_sql(assistant_reply)
                # Convert results to a string format for replying back

                result_str = "".join([str(t) for t in results])
                self.messages.append({'role': 'user', 'content': result_str})
                self.chat("DatabaseOutput-87948"+result_str)
                return result_str
            else:
                # Return the chatbot's response
                return assistant_reply
        else:
            return f"Error: {response.status_code} - {response.text}"

    def run_sql(self, query):
        query = query.replace(self.keyword, "").replace(self.keyword2, "")
        con = sqlite3.connect("tickets.db")
        cur = con.cursor()
        
        try:
            cur.execute(query)
            con.commit()
            results = cur.fetchall()
            return results
        except sqlite3.Error as e:
            return f"SQLite error: {e}"
        finally:
            con.close()


# Example usage
api_key = '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'
bot = GPT3Chatbot(api_key)
# bot.set_initial_prompt(initial_prompt)  # You would call this somewhere before engaging in chat
response = bot.chat("")
print(response)