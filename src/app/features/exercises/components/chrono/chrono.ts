import { ChangeDetectionStrategy, Component, OnDestroy, computed, input, signal } from '@angular/core';

/** Chronomètre d'entretien : compte le temps écoulé et passe en rouge au-delà de la durée conseillée. */
@Component({
  selector: 'app-chrono',
  templateUrl: './chrono.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Chrono implements OnDestroy {
  /** Durée conseillée, en minutes. */
  readonly minutes = input.required<number>();

  protected readonly elapsed = signal(0);
  protected readonly running = signal(false);
  private timer?: ReturnType<typeof setInterval>;

  protected readonly display = computed(() => `${format(this.elapsed())} / ${format(this.minutes() * 60)}`);
  protected readonly overtime = computed(() => this.elapsed() > this.minutes() * 60);

  protected toggle(): void {
    if (this.running()) {
      this.stop();
    } else {
      this.running.set(true);
      this.timer = setInterval(() => this.elapsed.update((s) => s + 1), 1000);
    }
  }

  protected reset(): void {
    this.stop();
    this.elapsed.set(0);
  }

  ngOnDestroy(): void {
    this.stop();
  }

  private stop(): void {
    clearInterval(this.timer);
    this.timer = undefined;
    this.running.set(false);
  }
}

function format(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}
