import { TestBed } from '@angular/core/testing';
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
});
