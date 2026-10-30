import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import type { TestResult } from '../../features/runner-ts';

@Component({
  selector: 'app-test-results',
  templateUrl: './test-results.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TestResults {
  readonly results = input<TestResult[] | null>(null);
  readonly running = input(false);

  protected readonly passedCount = computed(() => this.results()?.filter((r) => r.passed).length ?? 0);
  protected readonly allPassed = computed(() => {
    const r = this.results();
    return !!r && r.length > 0 && r.every((t) => t.passed);
  });
}
