import { Component } from '@angular/core';
import { AuthenticationService } from '../_service/authentication.service';

@Component({
    moduleId: module.id,
    selector: 'viewr',
    templateUrl: `viewr.component.html`
})
export class ViewRComponent {
    constructor(public authService: AuthenticationService) {}
}