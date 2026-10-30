export interface QuestionDto {
  id: string;
  category: string;
  difficulty: string;
  question: string;
  code?: string;
  options: string[];
  answer: number[];
  explanation: string;
  source?: string;
  license?: string;
}
