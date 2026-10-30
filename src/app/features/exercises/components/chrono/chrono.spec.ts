import { TestBed } from '@angular/core/testing';
import { Chrono } from './chrono';

describe('Chrono', () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  function setup(minutes = 1) {
    const fixture = TestBed.createComponent(Chrono);
    fixture.componentRef.setInput('minutes', minutes);
    fixture.detectChanges();
    const el = fixture.nativeElement as HTMLElement;
    const button = (label: string) => Array.from(el.querySelectorAll('button')).find((b) => b.textContent?.includes(label))!;
    const tick = (seconds: number) => {
      vi.advanceTimersByTime(seconds * 1000);
      fixture.detectChanges();
    };
    return { fixture, el, button, tick };
  }

  it('affiche 00:00 / durée conseillée au départ', () => {
    expect(setup(30).el.querySelector('[role="timer"]')?.textContent?.trim()).toBe('00:00 / 30:00');
  });

  it('compte les secondes après Démarrer, puis se met en pause', () => {
    const { el, button, tick, fixture } = setup();
    button('Démarrer').click();
    tick(65);
    expect(el.querySelector('[role="timer"]')?.textContent).toContain('01:05');
    button('Pause').click();
    fixture.detectChanges();
    tick(10);
    expect(el.querySelector('[role="timer"]')?.textContent).toContain('01:05');
    expect(button('Reprendre')).toBeTruthy();
  });

  it('signale le dépassement de la durée conseillée', () => {
    const { el, button, tick } = setup(1);
    button('Démarrer').click();
    tick(61);
    expect(el.textContent).toContain('Temps dépassé');
  });

  it('Remettre à zéro arrête et réinitialise', () => {
    const { el, button, tick, fixture } = setup();
    button('Démarrer').click();
    tick(5);
    button('Remettre à zéro').click();
    fixture.detectChanges();
    expect(el.querySelector('[role="timer"]')?.textContent).toContain('00:00');
    tick(5);
    expect(el.querySelector('[role="timer"]')?.textContent).toContain('00:00');
  });
});
