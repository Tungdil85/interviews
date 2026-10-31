import { TestBed } from '@angular/core/testing';
import { loadNodeTypescript } from '../../../../../testing/node-typescript';
import { RunnerAngularService } from './runner-angular.service';
import { TS_LOADER } from '../../typescript';

describe('RunnerAngularService', () => {
  let runner: RunnerAngularService;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [{ provide: TS_LOADER, useValue: loadNodeTypescript }] });
    runner = TestBed.inject(RunnerAngularService);
  });

  afterEach(() => runner.clear());

  const pipeCode = `
    import { Pipe, PipeTransform } from '@angular/core';
    @Pipe({ name: 'shout' })
    export class ShoutPipe implements PipeTransform {
      transform(value: string): string { return value.toUpperCase() + '!'; }
    }`;

  it('compile un pipe TypeScript décoré et le rend dans un template', async () => {
    const { results } = await runner.run(pipeCode, [
      { name: 'rendu', code: `const v = render('{{ t | shout }}', { imports: [ShoutPipe], props: { t: 'salut' } }); assert.equal(v.text(), 'SALUT!');` },
    ]);
    expect(results).toEqual([{ name: 'rendu', passed: true }]);
  });

  it('rend un composant avec signaux, gère les clics et la détection de changement', async () => {
    const code = `
      import { Component, signal } from '@angular/core';
      @Component({
        selector: 'app-counter',
        template: '<button id="inc" (click)="count.set(count() + 1)">+</button><p>{{ count() }}</p>',
      })
      export class Counter { count = signal(0); }`;
    const { results } = await runner.run(code, [
      { name: 'incrémente', code: `const v = render(Counter); v.click('#inc'); v.click('#inc'); assert.equal(v.text('p'), '2');` },
      { name: 'échec attendu', code: `const v = render(Counter); assert.equal(v.text('p'), '1');` },
    ]);
    expect(results[0].passed).toBe(true);
    expect(results[1].passed).toBe(false);
    expect(results[1].message).toContain('Attendu "1"');
  });

  it('exécute une directive avec HostListener et @Input', async () => {
    const code = `
      import { Directive, HostListener, ElementRef, Input, inject } from '@angular/core';
      @Directive({ selector: '[appHl]' })
      export class Hl {
        @Input() appHl = 'yellow';
        private el = inject(ElementRef);
        @HostListener('mouseenter') on() { this.el.nativeElement.style.backgroundColor = this.appHl; }
      }`;
    const { results } = await runner.run(code, [
      { name: 'survol', code: `const v = render('<p appHl="red">x</p>', { imports: [Hl] }); v.trigger('p', 'mouseenter'); assert.equal(v.query('p').style.backgroundColor, 'red');` },
    ]);
    expect(results).toEqual([{ name: 'survol', passed: true }]);
  });

  it('signale les erreurs de syntaxe et les modules inconnus', async () => {
    const syntax = await runner.run('class {', [{ name: 'x', code: '' }]);
    expect(syntax.results).toEqual([]);
    expect(syntax.compileErrors[0].message).toBeTruthy();
    const unknown = await runner.run(`import { x } from 'lodash'; x();`, [{ name: 'x', code: '' }]);
    expect(unknown.compileErrors[0].message).toContain('Module non disponible');
  });

  it('localise une erreur de syntaxe (ligne et colonne)', async () => {
    const { compileErrors } = await runner.run('const a = 1;\nconst b = ;\n', [{ name: 'x', code: '' }]);
    expect(compileErrors[0].line).toBe(2);
    expect(compileErrors[0].column).toBeGreaterThan(0);
  });

  it('signale une erreur levée au chargement du module, sans exécuter les tests', async () => {
    const report = await runner.run('throw new Error("boom au chargement");', [{ name: 'x', code: 'assert.ok(true)' }]);
    expect(report.results).toEqual([]);
    expect(report.compileErrors[0].message).toContain('boom au chargement');
  });

  it('remonte une erreur de template (propriété inconnue)', async () => {
    const { results } = await runner.run(pipeCode, [
      { name: 'pipe inconnu', code: `render('{{ t | nope }}', { imports: [ShoutPipe], props: { t: 'a' } });` },
    ]);
    expect(results[0].passed).toBe(false);
  });

  describe('renderLive (aperçu à la volée)', () => {
    const preview = () => {
      const el = document.createElement('div');
      document.body.appendChild(el);
      return el;
    };
    const previewCode = `render('{{ "salut" | shout }}', { imports: [ShoutPipe] });`;

    it('rend uniquement l’aperçu, sans exécuter de test', async () => {
      const el = preview();
      expect(await runner.renderLive(pipeCode, previewCode, el)).toEqual([]);
      expect(el.textContent).toContain('SALUT!');
      el.remove();
    });

    it('renvoie les erreurs de syntaxe et conserve l’ancien aperçu', async () => {
      const el = preview();
      await runner.renderLive(pipeCode, previewCode, el);
      const errors = await runner.renderLive('const a = ;', previewCode, el);
      expect(errors?.[0].line).toBe(1);
      expect(el.textContent).toContain('SALUT!');
      el.remove();
    });

    it('renvoie une erreur de compilation pour un template invalide', async () => {
      const el = preview();
      const errors = await runner.renderLive(pipeCode, `render('{{ t | nope }}', { imports: [ShoutPipe], props: { t: 'a' } });`, el);
      expect(errors?.[0].message).toMatch(/NG0\d+/);
      el.remove();
    });

    it('une erreur d’exécution de l’aperçu va dans la console, pas dans les erreurs de compilation', async () => {
      const el = preview();
      expect(await runner.renderLive(pipeCode, `throw new Error('plantage');`, el)).toEqual([]);
      expect(runner.logs().some((l) => l.level === 'error' && l.text.includes('plantage'))).toBe(true);
      el.remove();
    });

    it('ignore (null) un rendu remplacé par un plus récent', async () => {
      const el = preview();
      const first = runner.renderLive(pipeCode, previewCode, el);
      const second = runner.renderLive(pipeCode, previewCode, el);
      expect(await first).toBeNull();
      expect(await second).toEqual([]);
      expect(el.children).toHaveLength(1); // un seul composant rendu, pas de doublon
      el.remove();
    });

    it('un lancement des tests annule un rendu à la volée en cours', async () => {
      const el = preview();
      const live = runner.renderLive(pipeCode, previewCode, el);
      await runner.run(pipeCode, [{ name: 't', code: 'assert.ok(true)' }], el, previewCode);
      expect(await live).toBeNull();
      el.remove();
    });
  });
});
