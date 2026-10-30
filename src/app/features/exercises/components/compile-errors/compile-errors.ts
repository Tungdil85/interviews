import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import type { CompileError } from '../../models/test-result.model';

@Component({
  selector: 'app-compile-errors',
  templateUrl: './compile-errors.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CompileErrors {
  readonly errors = input<CompileError[]>([]);
}
