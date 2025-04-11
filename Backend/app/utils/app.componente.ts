import { Component, OnInit } from '@angular/core';
import { ProjectSchema } from './models/component.interface';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  project: ProjectSchema = {{ project | tojson }};
  
  constructor() { }
  
  ngOnInit(): void {
    console.log('Proyecto cargado:', this.project);
  }
}