import openai
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import quiz_kb, topic_kb, menu_kb
from states import QuizState
import re


router = Router()

# Function to generate a question based on the selected topic
async def get_quiz_question(topic: str):
    prompt = f"Ask a question about {topic} that has one correct answer. Suggest 3 possible answers, where only one of them is correct. Do not repeat questions!!! Don't give the correct answer before the user tried to answer" \
             f"Clearly indicate the correct answer in this format: 'Correct Answer: A) ...'."
    content = "You are a helpful quiz bot that generates quiz questions and their correct answers. Do not repeat questions!!!."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": prompt}
        ]
    )
    full_response = response["choices"][0]["message"]["content"]
    # Extracting question and correct answer
    match = re.search(r"Correct Answer:\s*([A-C])\)", full_response)
    if match:
        question = full_response[:match.start()].strip()
        correct_answer = match.group(1).strip()
    else:
        question = full_response.strip()
        correct_answer = "Unknown"

    return question, correct_answer
    #return response["choices"][0]["message"]["content"]

# Handle /quiz command to start the quiz
@router.message(Command("quiz"))
@router.message(lambda msg: msg.text == "Quiz")
async def start_quiz(message: Message, state: FSMContext):
    await state.set_state(QuizState.waiting_for_topic)
    await message.answer("Choose a topic for the quiz:", reply_markup=topic_kb)

# Function to send a new question
async def send_new_question(message: Message, state: FSMContext):
    data = await state.get_data()
    topic = data.get("topic")
    question, correct_answer = await get_quiz_question(topic)
    await state.update_data(last_question=question, correct_answer=correct_answer)
    await message.answer(question, reply_markup=quiz_kb)

# Handle stop quiz command
@router.message(lambda msg: msg.text.lower() == "stop quiz")
async def stop_quiz(message: Message, state: FSMContext):
    data = await state.get_data()
    correct_answers = data.get("correct_answers", 0)
    question_counter = data.get("user_answers", 0)
    await state.clear()  # Reset state
    await message.answer(f"Quiz ended! You got {correct_answers} correct answers from {question_counter} questions.", reply_markup=menu_kb)

# Handle topic selection
@router.message(QuizState.waiting_for_topic)
async def select_topic(message: Message, state: FSMContext):
    topic = message.text.lower()
    if topic in ['music', 'geography', 'python programming', 'history']:
        await state.update_data(topic=topic, correct_answers=0, user_answers=0)  # Initialize correct answers
        await state.set_state(QuizState.in_quiz)
        await send_new_question(message, state)
    else:
        await message.answer("Invalid topic. Please choose one of the available topics.")


# Function to check if user's answer is correct (with partial matching)
def is_answer_correct(user_answer: str, correct_answer: str) -> bool:
    user_answer = user_answer.lower().strip()
    correct_answer = correct_answer.lower().strip()

    return user_answer in correct_answer or correct_answer in user_answer

# Handle user's answer
@router.message(QuizState.in_quiz)
async def answer_quiz(message: Message, state: FSMContext):
    if message.text == "Next Question":
        await send_new_question(message, state)
        return
    elif message.text == "Stop Quiz":
        await stop_quiz(message, state)
        return

    data = await state.get_data()
    correct_answer = data.get("correct_answer")
    correct_answers = data.get("correct_answers", 0)
    user_answer = message.text.strip()
    question_counter = data.get("user_answers", 0)

    # Ensure answer is A, B, or C
    if user_answer not in ["A", "B", "C"]:
        await message.answer("⚠ Please choose only 'A', 'B', or 'C'.")
        return

    # Check if the user's answer is correct
    if user_answer == correct_answer:
        correct_answers += 1
        await message.answer("Correct!")
    else:
        await message.answer(f"Incorrect! The correct answer was: **{correct_answer}**")
    question_counter +=1
    await state.update_data(correct_answers=correct_answers)
    await state.update_data(user_answers=question_counter)

    # Show "Next Question" and "Stop Quiz" buttons
    await message.answer("Click 'Next Question' to continue or 'Stop Quiz' to end.", reply_markup=quiz_kb)

