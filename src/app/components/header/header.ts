import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-header',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './header.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Header {
  protected readonly links = [
    { path: '/quiz', label: 'QCM' },
    { path: '/exercises', label: 'Exercices' },
    { path: '/progress', label: 'Progression' },
    { path: '/credits', label: 'Crédits' },
  ];
}
