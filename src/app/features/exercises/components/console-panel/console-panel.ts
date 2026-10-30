import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import type { LogEntry } from '../../models/test-result.model';

@Component({
  selector: 'app-console-panel',
  templateUrl: './console-panel.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ConsolePanel {
  readonly logs = input<LogEntry[]>([]);
  readonly cleared = output<void>();

  protected readonly icons = { log: '›', info: 'ℹ', warn: '⚠', error: '✖' };

  protected levelClass(level: LogEntry['level']): string {
    switch (level) {
      case 'error':
        return 'text-red-300';
      case 'warn':
        return 'text-yellow-300';
      case 'info':
        return 'text-sky-300';
      default:
        return 'text-gray-100';
    }
  }
}
