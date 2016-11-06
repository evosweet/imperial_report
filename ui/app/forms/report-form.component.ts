import { Component } from '@angular/core';
import { Report } from '../model/report';
import { Image } from '../model/image';
import {  ReportMake } from '../model/reportMake';
import { ReportService } from '../_service/report.service';


@Component({
    moduleId: module.id,
    selector: 'report-from',
    templateUrl: `report-form.component.html`
})
export class ReportFormComponent {
    active = true;
    subResult: ReportMake;
    submitted = false;
    fileStatus = false;
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
            {'id': 11, 'event': 'FLOODING'},
            {'id': 12, 'event': 'ACCIDENTS'},
            {'id': 13, 'event': 'DEATH'},
            {'id': 14, 'event': 'WATER OUTAGE'},
            {'id': 15, 'event': 'VANDALISM'},
            {'id': 10, 'event': 'OTHER'},
        ]

    districts = [
        {'id': 1, 'district': "OUTSIDE GEORGETOWN"},
        {'id': 3, 'district': "PETER' S HALL"},
        {'id': 4, 'district': "QUEENSTOWN"},
        {'id': 5, 'district': "ALBERTTOWN"},
        {'id': 6, 'district': "SOUTH CUMMINGSBURG"},
        {'id': 7, 'district': "NORTH CUMMINGSBURG"}
    ]
    model = new Report(this.events[0].event, this.events[0].id, this.districts[0].id, this.districts[0].district , '', '');
    imageModel = new Image(0, '');
    constructor(private reportservice: ReportService, ) {}
    newReport() {
        this.model = new Report(this.events[0].event, this.events[0].id, this.districts[0].id, this.districts[0].district , '', '');
        this.active = false;
        setTimeout(() => this.active = true, 0);
         this.submitted = false;
    }
    onSubmit() {
        //event: number, location: string, description: string, district_id: number, phone?: string,email?: string, reportDate?: string
        this.reportservice.makeReport(this.model.event_id, this.model.location, this.model.description,this.model.district_id,
        this.model.phone, this.model.email, this.model.reportDate)
        .then( result => {
            if (result.result === 'ERROR') {
                console.log("error")
            } else {
                this.submitted = true;
                this.subResult = result.msg;
                this.imageModel.id = result.msg.reference_no;
            }
        });
    }
    onUpload() {
        this.imageModel.id = this.subResult.reference_no;
        this.reportservice.uploadImg(this.imageModel.id, this.imageModel.file)
        .then( result => {
             if (result.result === 'ERROR') {
                console.log("error")
            } else {
                this.submitted = true;
                this.fileStatus = true;
            }
        });
    }
    closeUpload() {
        this.imageModel = new Image(0, '');
        this.model = new Report(this.events[0].event, this.events[0].id, this.districts[0].id, this.districts[0].district , '', '');
        this.submitted = false;
        this.fileStatus = false;
    }
    onChange($event: any): void {
         this.fileStatus = false;
         var inputValue = $event.target;
         this.imageModel.file = inputValue.files[0];
    }
}
