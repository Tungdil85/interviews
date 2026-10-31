import { Service } from '@angular/core';
import type { Category, Difficulty, Question } from '@shared/question';
import type { QuestionDto } from './dto/question.dto';

@Service()
export class QuizMapper {
  toQuestion(dto: QuestionDto): Question {
    const correct = [...dto.answer].sort((a, b) => a - b);
    return {
      id: dto.id,
      category: dto.category as Category,
      difficulty: dto.difficulty as Difficulty,
      text: dto.question,
      code: dto.code,
      options: dto.options,
      correct,
      multiple: correct.length > 1,
      explanation: dto.explanation,
      source: dto.source,
      license: dto.license,
    };
  }
}
