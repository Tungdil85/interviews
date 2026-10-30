import { TestBed } from '@angular/core/testing';
import { Credits } from './credits';

describe('Credits', () => {
  it('s’affiche', () => {
    const fixture = TestBed.createComponent(Credits);
    fixture.detectChanges();
    const text = (fixture.nativeElement as HTMLElement).textContent;
    expect(text).toContain('Crédits et licences');
    expect(text).toContain('freeCodeCamp');
  });
});
