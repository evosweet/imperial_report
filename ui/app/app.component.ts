import { Component } from '@angular/core';
import { AuthenticationService } from './_service/authentication.service';

@Component({
    moduleId: module.id,
    selector: 'my-app',
    templateUrl: `app.component.html`
})
export class AppComponent {
    constructor(public authService: AuthenticationService) {}
}
