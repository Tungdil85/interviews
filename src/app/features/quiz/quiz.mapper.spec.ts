import { QuizMapper } from './quiz.mapper';
import type { QuestionDto } from './dto/question.dto';

describe('QuizMapper', () => {
  const mapper = new QuizMapper();
  const dto: QuestionDto = {
    id: 'a-1',
    category: 'angular',
    difficulty: 'easy',
    question: 'Q ?',
    options: ['a', 'b', 'c'],
    answer: [2, 0],
    explanation: 'parce que',
  };

  it('convertit le DTO en modèle et trie les bonnes réponses', () => {
    const q = mapper.toQuestion(dto);
    expect(q.text).toBe('Q ?');
    expect(q.correct).toEqual([0, 2]);
    expect(q.multiple).toBe(true);
  });

  it('une seule bonne réponse => choix unique', () => {
    expect(mapper.toQuestion({ ...dto, answer: [1] }).multiple).toBe(false);
  });

  it('conserve la source et la licence', () => {
    const q = mapper.toQuestion({ ...dto, source: 'repo', license: 'MIT' });
    expect(q.source).toBe('repo');
    expect(q.license).toBe('MIT');
  });
});
