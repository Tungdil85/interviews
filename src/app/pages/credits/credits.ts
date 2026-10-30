import { ChangeDetectionStrategy, Component } from '@angular/core';

interface Credit {
  name: string;
  url: string;
  license: string;
  note: string;
}

@Component({
  selector: 'app-credits',
  templateUrl: './credits.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Credits {
  /** Sources open source dont des questions ont été reprises (champ `source` / `license` dans les JSON). */
  protected readonly credits: Credit[] = [
    {
      name: 'freeCodeCamp/developer_quiz_site',
      url: 'https://github.com/freeCodeCamp/developer_quiz_site',
      license: 'BSD 3-Clause — Copyright (c) 2023, freeCodeCamp. All rights reserved.',
      note: 'Questions CSS (en anglais) reprises de src/data/css-quiz.ts, options remélangées. Redistribution avec conservation de cette notice de copyright, sans engagement ni caution de freeCodeCamp.',
    },
  ];
}
