## This module defines FSM states to track active sessions.

from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    RANDOM_FACT = State()
    CELEBRITY_CHAT = State()
    SELECTING_CELEBRITY = State()
    CHAT_GPT = State()

class QuizState(StatesGroup):
    waiting_for_topic = State()
    in_quiz = State()

