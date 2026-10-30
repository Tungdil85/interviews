import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', title: 'Accueil', loadComponent: () => import('./pages/home/home').then((m) => m.Home) },
  { path: 'quiz', title: 'QCM', loadComponent: () => import('./pages/quiz-setup/quiz-setup').then((m) => m.QuizSetup) },
  { path: 'quiz/play', title: 'QCM en cours', loadComponent: () => import('./pages/quiz-play/quiz-play').then((m) => m.QuizPlay) },
  { path: 'quiz/result', title: 'Résultat', loadComponent: () => import('./pages/quiz-result/quiz-result').then((m) => m.QuizResult) },
  { path: 'exercises', title: 'Exercices', loadComponent: () => import('./pages/exercises-list/exercises-list').then((m) => m.ExercisesList) },
  { path: 'exercises/:id', title: 'Exercice', loadComponent: () => import('./pages/exercise-detail/exercise-detail').then((m) => m.ExerciseDetail) },
  { path: 'progress', title: 'Progression', loadComponent: () => import('./pages/progress/progress').then((m) => m.Progress) },
  { path: 'credits', title: 'Crédits', loadComponent: () => import('./pages/credits/credits').then((m) => m.Credits) },
  { path: '**', redirectTo: '' },
];
