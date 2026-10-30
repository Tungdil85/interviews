import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { ProgressService } from '@features/progress';
import { Progress } from './progress';

describe('Progress', () => {
  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({ providers: [provideRouter([])] });
  });

  it('affiche une ligne par catégorie', () => {
    const fixture = TestBed.createComponent(Progress);
    fixture.detectChanges();
    expect((fixture.nativeElement as HTMLElement).querySelectorAll('[role="progressbar"]')).toHaveLength(4);
  });

  it('reflète les sessions enregistrées et propose la révision', () => {
    TestBed.inject(ProgressService).recordSession(
      { date: 1_700_000_000_000, mode: 'practice', total: 1, score: 0, durationMs: 1 },
      [{ id: 'x', category: 'css', correct: false }],
    );
    const fixture = TestBed.createComponent(Progress);
    fixture.detectChanges();
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('0/1');
    expect(text).toContain('Lancer une révision');
  });
});
