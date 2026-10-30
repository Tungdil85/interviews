import { TestBed } from '@angular/core/testing';
import { CompileErrors } from './compile-errors';

describe('CompileErrors', () => {
  function render(errors: { message: string; line?: number; column?: number }[]) {
    const fixture = TestBed.createComponent(CompileErrors);
    fixture.componentRef.setInput('errors', errors);
    fixture.detectChanges();
    return fixture.nativeElement as HTMLElement;
  }

  it('n’affiche rien sans erreur', () => {
    expect(render([]).querySelector('[role="alert"]')).toBeNull();
  });

  it('affiche le message avec la position', () => {
    const text = render([{ message: "';' attendu", line: 3, column: 7 }]).textContent;
    expect(text).toContain('1 erreur de compilation');
    expect(text).toContain('Ligne 3, colonne 7');
    expect(text).toContain("';' attendu");
  });

  it('accorde le pluriel et accepte une erreur sans position', () => {
    const text = render([{ message: 'a' }, { message: 'b' }]).textContent;
    expect(text).toContain('2 erreurs de compilation');
    expect(text).not.toContain('Ligne');
  });
});
