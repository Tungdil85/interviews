import { TestBed } from '@angular/core/testing';
import { StorageService } from './storage.service';

describe('StorageService', () => {
  let service: StorageService;

  beforeEach(() => {
    localStorage.clear();
    service = TestBed.inject(StorageService);
  });

  it('retourne la valeur par défaut si la clé est absente', () => {
    expect(service.get('absent', 42)).toBe(42);
  });

  it('écrit puis relit une valeur JSON', () => {
    service.set('k', { a: [1, 2] });
    expect(service.get('k', null)).toEqual({ a: [1, 2] });
  });

  it('retourne la valeur par défaut si le JSON est corrompu', () => {
    localStorage.setItem('k', '{pas du json');
    expect(service.get('k', 'défaut')).toBe('défaut');
  });

  it('supprime une clé', () => {
    service.set('k', 1);
    service.remove('k');
    expect(service.get('k', 0)).toBe(0);
  });
});
