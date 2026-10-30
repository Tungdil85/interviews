import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { Header } from './header';

describe('Header', () => {
  it('affiche la navigation principale', () => {
    TestBed.configureTestingModule({ providers: [provideRouter([])] });
    const fixture = TestBed.createComponent(Header);
    fixture.detectChanges();
    const el = fixture.nativeElement as HTMLElement;
    expect(el.querySelector('nav[aria-label="Navigation principale"]')).toBeTruthy();
    expect(el.querySelectorAll('nav a')).toHaveLength(5);
  });
});
