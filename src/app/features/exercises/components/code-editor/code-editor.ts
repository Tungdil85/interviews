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
import { indentLess, indentMore } from '@codemirror/commands';
import { javascript } from '@codemirror/lang-javascript';
import { indentUnit } from '@codemirror/language';
import { oneDark } from '@codemirror/theme-one-dark';
import { keymap } from '@codemirror/view';
import type { EditorView as View } from '@codemirror/view';
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
  /** Après Échap, Tab quitte l'éditeur (sinon un utilisateur au clavier y resterait piégé). */
  private tabEscapes = false;

  constructor() {
    afterNextRender(() => {
      this.view = new EditorView({
        doc: this.code(),
        parent: this.host().nativeElement,
        extensions: [
          // Avant basicSetup : Tab / Maj+Tab indentent au lieu de déplacer le focus vers le bouton suivant.
          keymap.of([
            {
              key: 'Escape',
              run: () => (this.tabEscapes = true),
            },
            {
              key: 'Tab',
              run: (view) => !this.tabEscapes && this.indent(view),
              shift: (view) => !this.tabEscapes && indentLess(view),
            },
          ]),
          EditorView.domEventHandlers({
            blur: () => void (this.tabEscapes = false),
            keydown: (event) => void (event.key !== 'Escape' && event.key !== 'Tab' && event.key !== 'Shift' && (this.tabEscapes = false)),
          }),
          basicSetup,
          javascript({ typescript: true }),
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

  /** Sans sélection : insère l'unité d'indentation (2 espaces) au curseur ; avec : indente les lignes. */
  private indent(view: View): boolean {
    if (view.state.selection.ranges.some((range) => !range.empty)) return indentMore(view);
    view.dispatch(view.state.update(view.state.replaceSelection(view.state.facet(indentUnit)), { scrollIntoView: true, userEvent: 'input' }));
    return true;
  }

  ngOnDestroy(): void {
    this.view?.destroy();
  }
}
