import {
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  OnDestroy,
  afterNextRender,
  effect,
  input,
  model,
  viewChild,
} from '@angular/core';
import { javascript } from '@codemirror/lang-javascript';
import { oneDark } from '@codemirror/theme-one-dark';
import { EditorView, basicSetup } from 'codemirror';

@Component({
  selector: 'app-code-editor',
  templateUrl: './code-editor.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CodeEditor implements OnDestroy {
  readonly code = model('');
  readonly ariaLabel = input('Éditeur de code');

  private readonly host = viewChild.required<ElementRef<HTMLElement>>('host');
  private view?: EditorView;

  constructor() {
    afterNextRender(() => {
      this.view = new EditorView({
        doc: this.code(),
        parent: this.host().nativeElement,
        extensions: [
          basicSetup,
          javascript(),
          oneDark,
          EditorView.contentAttributes.of({ 'aria-label': this.ariaLabel() }),
          EditorView.updateListener.of((update) => {
            if (update.docChanged) this.code.set(update.state.doc.toString());
          }),
        ],
      });
    });

    // Synchronise les changements externes (ex. « Réinitialiser ») vers l'éditeur.
    effect(() => {
      const value = this.code();
      const view = this.view;
      if (view && view.state.doc.toString() !== value) {
        view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: value } });
      }
    });
  }

  ngOnDestroy(): void {
    this.view?.destroy();
  }
}
