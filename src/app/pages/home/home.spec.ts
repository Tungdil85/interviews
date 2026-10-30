import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { Home } from './home';

describe('Home', () => {
  it('affiche les quatre entrées principales', () => {
    localStorage.clear();
    TestBed.configureTestingModule({ providers: [provideRouter([])] });
    const fixture = TestBed.createComponent(Home);
    fixture.detectChanges();
    const el = fixture.nativeElement as HTMLElement;
    expect(el.querySelectorAll('a')).toHaveLength(4);
    expect(el.textContent).toContain('Prépare ton entretien');
  });
});
