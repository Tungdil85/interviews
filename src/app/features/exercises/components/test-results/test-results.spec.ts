import { TestBed } from '@angular/core/testing';
import { TestResults } from './test-results';

describe('TestResults', () => {
  function render(inputs: Record<string, unknown>) {
    const fixture = TestBed.createComponent(TestResults);
    for (const [k, v] of Object.entries(inputs)) fixture.componentRef.setInput(k, v);
    fixture.detectChanges();
    return (fixture.nativeElement as HTMLElement).textContent ?? '';
  }

  it('invite à lancer les tests quand il n’y a pas de résultat', () => {
    expect(render({})).toContain('Lance les tests');
  });

  it('affiche le décompte et le message d’erreur', () => {
    const text = render({
      results: [
        { name: 'a', passed: true },
        { name: 'b', passed: false, message: 'Attendu 1' },
      ],
    });
    expect(text).toContain('1 / 2 tests réussis');
    expect(text).toContain('Attendu 1');
    expect(text).not.toContain('bravo');
  });

  it('félicite quand tout passe', () => {
    expect(render({ results: [{ name: 'a', passed: true }] })).toContain('bravo');
  });

  it('indique l’exécution en cours', () => {
    expect(render({ running: true })).toContain('Exécution');
  });
});
