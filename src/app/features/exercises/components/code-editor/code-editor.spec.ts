import { TestBed } from '@angular/core/testing';
import { EditorView } from 'codemirror';
import { CodeEditor } from './code-editor';

describe('CodeEditor', () => {
  it('monte CodeMirror avec le code initial', async () => {
    const fixture = TestBed.createComponent(CodeEditor);
    fixture.componentRef.setInput('code', 'const a = 1;');
    fixture.detectChanges();
    await fixture.whenStable();
    const el = fixture.nativeElement as HTMLElement;
    expect(el.querySelector('.cm-editor')).toBeTruthy();
    expect(el.textContent).toContain('const a = 1;');
  });

  async function setup(code: string) {
    const fixture = TestBed.createComponent(CodeEditor);
    fixture.componentRef.setInput('code', code);
    fixture.detectChanges();
    await fixture.whenStable();
    const content = (fixture.nativeElement as HTMLElement).querySelector<HTMLElement>('.cm-content')!;
    const view = EditorView.findFromDOM((fixture.nativeElement as HTMLElement).querySelector('.cm-editor') as HTMLElement)!;
    const press = (key: string, shiftKey = false) => {
      const event = new KeyboardEvent('keydown', { key, shiftKey, bubbles: true, cancelable: true });
      content.dispatchEvent(event);
      return event;
    };
    return { fixture, view, press };
  }

  it('Tab insère une indentation dans le texte au lieu de changer le focus', async () => {
    const { view, press } = await setup('a');
    view.dispatch({ selection: { anchor: 1 } });
    const event = press('Tab');
    expect(event.defaultPrevented).toBe(true);
    expect(view.state.doc.toString()).toBe('a  ');
  });

  it('Tab avec une sélection indente les lignes sélectionnées', async () => {
    const { view, press } = await setup('a\nb');
    view.dispatch({ selection: { anchor: 0, head: 3 } });
    press('Tab');
    expect(view.state.doc.toString()).toBe('  a\n  b');
  });

  it('Maj+Tab désindente la ligne', async () => {
    const { view, press } = await setup('    x');
    view.dispatch({ selection: { anchor: 5 } });
    press('Tab', true);
    expect(view.state.doc.toString()).toBe('  x');
  });

  it('Échap puis Tab laisse le navigateur déplacer le focus', async () => {
    const { view, press } = await setup('a');
    press('Escape');
    const event = press('Tab');
    expect(event.defaultPrevented).toBe(false);
    expect(view.state.doc.toString()).toBe('a');
  });
});
