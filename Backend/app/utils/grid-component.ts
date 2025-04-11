import { Component, Input } from '@angular/core';
import { GridComponent } from '../../models/component.interface';

@Component({
  selector: 'app-grid-component',
  templateUrl: './grid-component.component.html',
  styleUrls: ['./grid-component.component.scss']
})
export class GridComponentComponent {
  @Input() data: GridComponent;
  
  get gridStyles() {
    return {
      display: 'grid',
      'grid-template-columns': `repeat(${this.data.columns}, 1fr)`,
      'grid-template-rows': `repeat(${this.data.rows}, auto)`,
      gap: this.data.gap || '0px'
    };
  }
}