import { Injectable } from '@angular/core';

/** Wrapper tolérant autour de localStorage (indisponible en navigation privée, SSR, tests…). */
@Injectable({ providedIn: 'root' })
export class StorageService {
  get<T>(key: string, fallback: T): T {
    try {
      const raw = localStorage.getItem(key);
      return raw === null ? fallback : (JSON.parse(raw) as T);
    } catch {
      return fallback;
    }
  }

  set<T>(key: string, value: T): void {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch {
      // quota dépassé ou stockage indisponible : on ignore volontairement
    }
  }

  remove(key: string): void {
    try {
      localStorage.removeItem(key);
    } catch {
      // idem
    }
  }
}
