import { NgTemplateOutlet } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';

interface Inline {
  text: string;
  kind: 'text' | 'code' | 'bold';
}

type Block =
  | { type: 'paragraph'; lines: Inline[][] }
  | { type: 'list'; items: Inline[][] }
  | { type: 'code'; text: string };

const INLINE_TOKEN = /(`[^`]+`|\*\*[^*]+\*\*)/;

/** Découpe une ligne en segments texte / `code` / **gras**. */
export function parseInline(line: string): Inline[] {
  return line
    .split(INLINE_TOKEN)
    .filter((part) => part !== '')
    .map((part): Inline => {
      if (part.startsWith('`') && part.endsWith('`') && part.length > 2) return { kind: 'code', text: part.slice(1, -1) };
      if (part.startsWith('**') && part.endsWith('**') && part.length > 4) return { kind: 'bold', text: part.slice(2, -2) };
      return { kind: 'text', text: part };
    });
}

/**
 * Mini-format des consignes : paragraphes, listes (lignes commençant par « • » ou « - »),
 * blocs de code entre ``` et `code` / **gras** en ligne. Rendu sans innerHTML.
 */
export function parseDescription(source: string): Block[] {
  const blocks: Block[] = [];
  const lines = source.split('\n');
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (line.trim().startsWith('```')) {
      const code: string[] = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith('```')) code.push(lines[i++]);
      i++; // fence fermante
      blocks.push({ type: 'code', text: code.join('\n') });
    } else if (/^\s*(•|- )/.test(line)) {
      const items: Inline[][] = [];
      while (i < lines.length && /^\s*(•|- )/.test(lines[i])) items.push(parseInline(lines[i++].replace(/^\s*(•|- )\s*/, '')));
      blocks.push({ type: 'list', items });
    } else if (line.trim() === '') {
      i++;
    } else {
      const paragraph: Inline[][] = [];
      while (i < lines.length && lines[i].trim() !== '' && !lines[i].trim().startsWith('```') && !/^\s*(•|- )/.test(lines[i])) {
        paragraph.push(parseInline(lines[i++]));
      }
      blocks.push({ type: 'paragraph', lines: paragraph });
    }
  }
  return blocks;
}

@Component({
  selector: 'app-exercise-description',
  imports: [NgTemplateOutlet],
  templateUrl: './exercise-description.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExerciseDescription {
  readonly text = input.required<string>();
  protected readonly blocks = computed(() => parseDescription(this.text()));
}
