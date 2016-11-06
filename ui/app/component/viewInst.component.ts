import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../_service/authentication.service';

@Component({
    moduleId: module.id,
    selector: 'viewinst',
    templateUrl: `viewinst.component.html`,
    styleUrls:[ '../../styles.css']
})
export class ViewinstComponent {
      currentUser: any;
      ngOnInit() {
          this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
      }
     
     constructor(public authService: AuthenticationService) {}

}