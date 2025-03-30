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


class RecommendationState(StatesGroup):
    choosing_category = State()
    choosing_genre = State()
    receiving_recommendation = State()


class VocabularyState(StatesGroup):
    learning = State()
    training = State()