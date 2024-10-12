# Instruction Following Game 🎮🧠

Instruction Following Game is an engaging and educational project designed to help users improve their prompt engineering skills and gain a deeper understanding of Large Language Models (LLMs). By challenging players to craft precise prompts that elicit specific responses from an LLM, this game offers a fun and interactive way to explore the nuances of AI communication.

## Features 🚀

- Web-based interface using Gradio
- Multiple challenging questions to test prompt engineering skills
- Real-time interaction with a powerful LLM (Qwen1.5-72B-Chat)
- User authentication and progress tracking
- Leaderboard to showcase top performers
- Detailed feedback on each submission

## How It Works 🛠️

1. **User Authentication**: Players start by entering a unique User ID.
2. **Question Selection**: Choose from a variety of predefined questions.
3. **Prompt Crafting**: Create a prompt that will make the LLM respond in a specific way.
4. **AI Interaction**: The prompt is sent to the LLM, which generates a response.
5. **Evaluation**: The system checks if the AI's response meets the question's criteria.
6. **Feedback**: Players receive immediate feedback on their performance.
7. **Progress Tracking**: Completed questions and attempt history are saved.
8. **Leaderboard**: A real-time leaderboard shows top performers.

## Technical Stack 💻

- **Backend**: Python
- **Frontend**: Gradio (for the web interface)
- **Database**: MongoDB (for user data and leaderboard)
- **LLM API**: Together.ai (using the Qwen1.5-72B-Chat model)
- **Additional Libraries**: requests, pymongo, logging

## Setup and Installation 🔧

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/instruction-following-game.git
   cd instruction-following-game
   ```

2. Install required packages:
   ```
   pip install gradio pymongo requests
   ```

3. Set up MongoDB:
   - Create a MongoDB Atlas account or use a local MongoDB instance
   - Update the MongoDB connection string in `main.py`

4. Set up Together.ai API:
   - Create an account at [Together.ai](https://www.together.ai/)
   - Replace the API key in `main.py` with your own key

5. Run the application:
   ```
   python main.py
   ```

## Usage 🎯

1. Open the provided URL in your web browser.
2. Enter a User ID to log in.
3. Select a question from the dropdown menu.
4. Craft your prompt in the input box.
5. Click "Submit" to send your prompt to the AI.
6. Review the AI's response and the feedback.
7. Keep trying until you successfully complete the challenge!
- Shoutout to the Gradio team for their excellent web UI framework.
- Special thanks to all the prompt engineers and AI enthusiasts who inspire projects like this!

Happy prompting, and may the best engineer win! 🏆🎉
