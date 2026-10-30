import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import type { Category } from '@shared/question';
import type { QuestionDto } from './dto/question.dto';

@Injectable({ providedIn: 'root' })
export class QuizGateway {
  private readonly http = inject(HttpClient);

  fetchCategory(category: Category): Observable<QuestionDto[]> {
    return this.http.get<QuestionDto[]>(`data/qcm-${category}.json`);
  }
}
