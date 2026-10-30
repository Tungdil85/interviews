import { categoryLabel, difficultyLabel } from './question.model';

describe('question.model', () => {
  it('retourne les libellés connus', () => {
    expect(categoryLabel('rxjs')).toBe('RxJS');
    expect(difficultyLabel('hard')).toBe('Difficile');
  });
});
