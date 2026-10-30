import { TestBed } from '@angular/core/testing';
import { ConsolePanel } from './console-panel';

describe('ConsolePanel', () => {
  function setup(logs: { level: 'log' | 'info' | 'warn' | 'error'; text: string }[]) {
    const fixture = TestBed.createComponent(ConsolePanel);
    fixture.componentRef.setInput('logs', logs);
    fixture.detectChanges();
    return fixture;
  }

  it('affiche un message d’aide quand la console est vide', () => {
    const fixture = setup([]);
    expect((fixture.nativeElement as HTMLElement).textContent).toContain('console.log()');
  });

  it('liste les entrées avec leur niveau', () => {
    const el = setup([{ level: 'log', text: 'bonjour' }, { level: 'error', text: 'oups' }]).nativeElement as HTMLElement;
    const items = el.querySelectorAll('li');
    expect(items).toHaveLength(2);
    expect(items[1].textContent).toContain('error');
    expect(items[1].className).toContain('text-red-300');
  });

  it('émet cleared au clic sur Effacer', () => {
    const fixture = setup([{ level: 'log', text: 'x' }]);
    let count = 0;
    fixture.componentInstance.cleared.subscribe(() => count++);
    (fixture.nativeElement as HTMLElement).querySelector('button')!.click();
    expect(count).toBe(1);
  });

  it('désactive Effacer quand il n’y a rien à effacer', () => {
    expect(((setup([]).nativeElement) as HTMLElement).querySelector('button')!.disabled).toBe(true);
  });
});
