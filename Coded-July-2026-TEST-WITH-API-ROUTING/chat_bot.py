# THIS SOFTWARE IS PROTECTED BY COPYRIGHT. UNAUTHORIZED USE, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED AND MAY RESULT IN LEGAL ACTION.

import requests
import tiktoken


class ChatAgent:

    def __init__(
        self,
        model="gpt-3.5-turbo",
        token_limit=4096,
        summary_size=300
    ):

        self.model = model
        self.messages = []
        self.token_limit = token_limit
        self.enc = tiktoken.encoding_for_model(self.model)
        self.primary_directive = None
        self.summary_size = summary_size

        # CHANGE THIS TO YOUR CLOUD RUN URL
        self.api_url = "https://coded-routing-775404256133.us-east1.run.app/api/chat"


    def set_primary_directive(self, system_prompt=None):

        if system_prompt:

            self.messages.append({
                "role": "system",
                "content": system_prompt
            })

            self.primary_directive = system_prompt


    def add_context(self, system_prompt=None):

        if system_prompt:

            self.messages.append({
                "role": "system",
                "content": system_prompt
            })


    def add_context_document(self, txt_doc):

        with open(txt_doc, "r") as file:

            content = file.read()

        self.messages.append({
            "role": "system",
            "content": content
        })


    def count_tokens(self):

        num_tokens = 0

        for message in self.messages:

            num_tokens += len(
                self.enc.encode(message["content"])
            )

        return num_tokens


    def tokens_left(self):

        return self.token_limit - self.count_tokens()


    def is_within_token_limit(self):

        return self.count_tokens() <= self.token_limit


    def chat(self, user_message):

        # Add user's message to history

        self.messages.append({
            "role": "user",
            "content": user_message
        })


        try:

            response = requests.post(
                self.api_url,
                json={
                    "messages": self.messages,
                    "model": self.model
                },
                timeout=30
            )


            response.raise_for_status()


            data = response.json()


            ai_message = data["response"]


        except Exception as e:

            print("Chat server error:", e)

            return "Sorry, I could not connect to the AI server."


        self.messages.append({
            "role": "assistant",
            "content": ai_message
        })


        return ai_message



    def get_conversation_history(self):

        return self.messages



    def clear_history(self):

        self.messages = []

        if self.primary_directive:

            self.set_primary_directive(
                self.primary_directive
            )



    def __repr__(self):

        return (
            f"ChatAgent("
            f"model='{self.model}', "
            f"messages={len(self.messages)}"
            f")"
        )



# TESTING ONLY
if __name__ == "__main__":


    agent = ChatAgent()


    agent.set_primary_directive(
        "You are an AI assistant that helps users."
    )


    agent.add_context(
        "You are a friendly robot."
    )


    while True:

        user_input = input("You: ")

        if user_input.lower() in [
            "bye",
            "quit",
            "exit"
        ]:
            break


        response = agent.chat(user_input)

        print("Agent:", response)



























