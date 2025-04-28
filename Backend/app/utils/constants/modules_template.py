NO_STAND_ALONE_DEFAULT = {
    "app_module_ts" : 
    """
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@NgModule({
declarations: [
    AppComponent
],
imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    CommonModule
],
providers: [],
bootstrap: [AppComponent]
})
export class AppModule { }
""",
"app_component_ts":
"""
import { Component } from '@angular/core';

@Component({
selector: 'app-root',
templateUrl: './app.component.html',
styleUrl: './app.component.css'
})
export class AppComponent {
    
}
    """,
    "app_componet_html":
    """
    
<router-outlet />
    """
}