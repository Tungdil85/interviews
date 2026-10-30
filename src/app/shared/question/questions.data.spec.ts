import { readFileSync } from 'node:fs';
import { CATEGORIES } from './question.model';
import type { QuestionDto } from '../../features/quiz/dto/question.dto';

describe.each(CATEGORIES.map((c) => c.id))('qcm-%s.json', (category) => {
  const questions = JSON.parse(readFileSync(`public/data/qcm-${category}.json`, 'utf-8')) as QuestionDto[];

  it('contient des questions de la bonne catégorie, avec des ids uniques', () => {
    expect(questions.length).toBeGreaterThan(0);
    expect(new Set(questions.map((q) => q.id)).size).toBe(questions.length);
    expect(questions.every((q) => q.category === category)).toBe(true);
  });

  it('chaque question est bien formée', () => {
    for (const q of questions) {
      expect(q.question.length, q.id).toBeGreaterThan(5);
      expect(q.options.length, q.id).toBeGreaterThanOrEqual(2);
      expect(new Set(q.options).size, `${q.id} options dupliquées`).toBe(q.options.length);
      expect(q.answer.length, q.id).toBeGreaterThan(0);
      expect(q.answer.every((i) => Number.isInteger(i) && i >= 0 && i < q.options.length), q.id).toBe(true);
      expect(['easy', 'medium', 'hard']).toContain(q.difficulty);
      expect(q.explanation.length, q.id).toBeGreaterThan(0);
    }
  });

  it('toute question importée mentionne sa source et sa licence', () => {
    for (const q of questions.filter((x) => x.source || x.license)) {
      expect(q.source && q.license, q.id).toBeTruthy();
    }
  });
});
