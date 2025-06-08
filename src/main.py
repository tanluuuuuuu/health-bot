from src.agent.graph import app

user_input = input("Enter your health topic: ")
app.invoke({"topic": user_input})
