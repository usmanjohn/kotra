import django
import os

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kotrain.settings")
django.setup()

from django.db import transaction
from exam.models import Test, Question, Choice

# Your script goes here

# Create a test
test = Test.objects.create(title="52nd Test of Proficiency in Korean", description="Reading section of the 52nd TOPIK")

# Questions and choices
questions_data = [
    {
        "question_text": "해가 뜨는 것을 ( ) 아침 일찍 일어났다.",
        "question_type": "MC",
        "choices": [
            {"choice_text": "보아야", "is_correct": False},
            {"choice_text": "보려고", "is_correct": True},
            {"choice_text": "보거나", "is_correct": False},
            {"choice_text": "보는데", "is_correct": False},
        ]
    },
    {
        "question_text": "무슨 일을 ( ) 열심히 하는 것이 중요하다.",
        "question_type": "MC",
        "choices": [
            {"choice_text": "하든지", "is_correct": True},
            {"choice_text": "하다가", "is_correct": False},
        ]
    },
     {
        "question_text": "신선한 재료! 부담 없는 가격! 가족 모임, 단체 환영",
        "question_type": "MC",
        "choices": [
            {"choice_text": "자연 보호", "is_correct": False},
            {"choice_text": "시간 절약", "is_correct": True},
            {"choice_text": "자리 양보", "is_correct": False},
            {"choice_text": "안전 관리", "is_correct": False},
        ]
    },
    {
        "question_text": "덩오후 1시까지 구매하면 그날 가져다 드립니다.",
        "question_type": "MC",
        "choices": [
            {"choice_text": "사용 설명", "is_correct": False},
            {"choice_text": "배달 안내", "is_correct": True},
            {"choice_text": "이용 순서", "is_correct": False},
            {"choice_text": "교환 방법", "is_correct": False},
        ]
    },
    {
        "question_text": "직업의 안정성을 중요하게 생각하는 사람이 가장 적다.",
        "question_type": "MC",
        "choices": [
            {"choice_text": "있는 척한다", "is_correct": False},
            {"choice_text": "있을 뿐이다", "is_correct": False},
            {"choice_text": "있을 지경이다", "is_correct": False},
            {"choice_text": "있는 모양이다", "is_correct": True},
        ]
    },
    {
        "question_text": "지난 13일 인주경찰서에 편지 한 통이 배달되었다.",
        "question_type": "MC",
        "choices": [
            {"choice_text": "관광객이 경찰에게 감사하는 마음을 표현했다.", "is_correct": True},
            {"choice_text": "관광객이 잃어버린 지갑을 찾지 못하고 돌아갔다.", "is_correct": False},
            {"choice_text": "경찰이 지갑을 잃어버린 관광객에게 편지를 썼다.", "is_correct": False},
            {"choice_text": "경찰이 관광객의 말을 이해하지 못해 도와줄 수 없었다.", "is_correct": False},
        ]
    },
    {
        "question_text": "최근 공연을 혼자 보는 사람들이 많아졌다.",
        "question_type": "MC",
        "choices": [
            {"choice_text": "있는 척한다", "is_correct": False},
            {"choice_text": "있을 뿐이다", "is_correct": False},
            {"choice_text": "있을 지경이다", "is_correct": False},
            {"choice_text": "있는 모양이다", "is_correct": True},
        ]
    },
    # Add remaining questions here following the same format
]

with transaction.atomic():
    for question_data in questions_data:
        question = Question.objects.create(
            test=test,
            question_text=question_data["question_text"],
            question_type=question_data["question_type"]
        )
        choices = [
            Choice(question=question, **choice_data)
            for choice_data in question_data["choices"]
        ]
        Choice.objects.bulk_create(choices)
