import { TestBed } from '@angular/core/testing';
import { ExerciseDescription, parseDescription, parseInline } from './exercise-description';

describe('parseInline', () => {
  it('sépare texte, code et gras', () => {
    expect(parseInline('Un `pipe` et du **gras** ici')).toEqual([
      { kind: 'text', text: 'Un ' },
      { kind: 'code', text: 'pipe' },
      { kind: 'text', text: ' et du ' },
      { kind: 'bold', text: 'gras' },
      { kind: 'text', text: ' ici' },
    ]);
  });

  it('laisse un texte sans marqueur intact', () => {
    expect(parseInline('rien de spécial')).toEqual([{ kind: 'text', text: 'rien de spécial' }]);
  });
});

describe('parseDescription', () => {
  it('reconnaît paragraphes, blocs de code et listes', () => {
    const blocks = parseDescription('Objectif\n\n```html\n<p>x</p>\n```\n\n• un\n• deux\nsuite');
    expect(blocks.map((b) => b.type)).toEqual(['paragraph', 'code', 'list', 'paragraph']);
    expect(blocks[1]).toEqual({ type: 'code', text: '<p>x</p>' });
    expect(blocks[2].type === 'list' && blocks[2].items).toHaveLength(2);
  });

  it('ne casse pas sur un bloc de code non fermé', () => {
    expect(parseDescription('```\nabc')).toEqual([{ type: 'code', text: 'abc' }]);
  });
});

describe('ExerciseDescription', () => {
  it('rend le code dans un <pre> et les listes en <li>, sans interpréter le HTML', () => {
    const fixture = TestBed.createComponent(ExerciseDescription);
    fixture.componentRef.setInput('text', 'Salut `x`\n\n```html\n<script>alert(1)</script>\n```\n\n• point **fort**');
    fixture.detectChanges();
    const el = fixture.nativeElement as HTMLElement;
    expect(el.querySelector('pre code')?.textContent).toBe('<script>alert(1)</script>');
    expect(el.querySelector('script')).toBeNull();
    expect(el.querySelector('li strong')?.textContent).toBe('fort');
    expect(el.querySelector('p code')?.textContent).toBe('x');
  });
});
