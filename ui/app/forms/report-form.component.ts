import { Component } from '@angular/core';
import { Report } from '../model/report';
import { Event } from '../model/event';


@Component({
    moduleId: module.id,
    selector: 'report-from',
    templateUrl: `report-form.component.html`
})
export class ReportFormComponent {
    active = true;
    events = [
            {'id': 1, 'event': 'Fire'},
            {'id': 2, 'event':  'DOMESTIC VIOLENCE'},
            {'id': 3, 'event': 'ROBBERY'},
            {'id': 4, 'event': 'NOISE COMPLAINT'},
            {'id': 5, 'event': 'POLLUTION'},
            {'id': 6, 'event': 'POWER OUTAGE'},
            {'id': 7, 'event': 'POT HOLES'},
            {'id': 8, 'event': 'HOMICIDE'},
            {'id': 9, 'event': 'SUSPICIOUS ACTIVITY'},
            {'id': 10, 'event': 'OTHER'},
            {'id': 11, 'event': 'FLOODING'},
            {'id': 12, 'event': 'ACCIDENTS'},
            {'id': 13, 'event': 'DEATH'},
            {'id': 14, 'event': 'WATER OUTAGE'},
            {'id': 15, 'event': 'VANDALISM'}
        ]
    model = new Report(this.events[0].event,'','');

    newReport() {
        this.model = new Report(this.events[0].event,'','');
        this.active = false;
        setTimeout(() => this.active = true, 0);
    }
    onSubmit(){
        alert("test");
    }
}
