import { Component } from '@angular/core';
import { Create } from '../../model/create';
import { ReportService } from '../../_service/report.service';
import { AuthenticationService } from '../../_service/authentication.service';
@Component({
    moduleId: module.id,
    selector: 'create',
    templateUrl: `create.component.html`
})
export class CreateComponent {
    authType = [
        {'id': 1, 'name': 'Ministry of Agriculture'},
        {'id': 2, 'name': 'Ministry of Business'},
        {'id': 3, 'name': 'Ministry of Communities'},
        {'id': 4, 'name': 'Ministry of Education'},
        {'id': 5, 'name': 'Ministry of Finance'},
        {'id': 6, 'name': 'Ministry of Foreign Affairs'},
        {'id': 7, 'name': 'Ministry of Indigenous Peoples Affairs'},
        {'id': 8, 'name': 'Ministry of Legal Affairs'},
        {'id': 9, 'name': 'Ministry of Natural Resources'},
        {'id': 10, 'name': ' Ministry of Public Health'},
        {'id': 11, 'name': ' Ministry of Public Infrastructure'},
        {'id': 12, 'name': ' Ministry of Public Security'},
        {'id': 13, 'name': ' Ministry of Social Protection'},
        {'id': 14, 'name': ' Ministry of the Presidency'},
        {'id': 15, 'name': ' Guyana Prison Service'},
        {'id': 16, 'name': ' Guyana Police Force'},
        {'id': 17, 'name': ' Guyana Fire Service'},
        {'id': 18, 'name': ' Ambulance'},
        {'id': 19, 'name': ' Guyana Telephone Telegraph'},
        {'id': 20, 'name': ' Digicel'},
        {'id': 21, 'name': ' Guyana Power & Light'},
        {'id': 22, 'name': 'Guyana Water Inc'},
        {'id': 23, 'name': 'Davis Memorial Hospital'},
        {'id': 24, 'name': 'Georgetown Public Hospital Corporation'},
        {'id': 25, 'name': 'Cheddi Jagan International Airport'},
        {'id': 26, 'name': 'Guyana Revenue Authority'},
        {'id': 32, 'name': 'Admin'}
    ]
    model = new Create('', this.authType[1].name, this.authType[1].id);
    errorMsg: string;
    returnData: string;
    constructor(private reportservice: ReportService, public authService: AuthenticationService ) {}
    onSubmit() {
        this.reportservice.createUser(this.model.username, this.model.id)
        .then( result => {
            if (result.result === 'ERROR') {
                this.errorMsg = result.result;
            } else {
                this.returnData = 'User Created';
            }
        });
    }
}
