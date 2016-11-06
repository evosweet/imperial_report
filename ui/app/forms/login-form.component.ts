import { Component, OnInit } from '@angular/core';
import { User } from '../model/user';
import { Router } from '@angular/router';
import { AuthenticationService } from '../_service/authentication.service';

@Component({
    moduleId: module.id,
    selector: 'login-form',
    templateUrl: `login-form.component.html`
})
export class LoginFormComponent {
    model = new User('', '');
    loading = false;
    errorMsg = '';
    constructor( private router: Router, private authenticationService: AuthenticationService ) {}

    ngOnInit() {
          this.authenticationService.logout();
    }

    login() {
          this.loading = true;
          this.authenticationService.login(this.model.username, this.model.password)
            .subscribe(result => {
                if (result === true) {
                    this.model.username = '';
                    this.model.password = '';
                    this.router.navigate(['/viewinst']);
                }else {
                    this.errorMsg = 'Username or password is incorrect';
                    this.loading = false;
                }
            });
      }
}
