import { Component } from '@angular/core';
import { Report } from '../../model/report';
import { MySearch } from '../../model/mysearch';
import { ReportService } from '../../_service/report.service';
import { ReportMake } from '../../model/reportMake';


@Component({
    moduleId: module.id,
    selector: 'edit',
    templateUrl: `edit.component.html`
})
export class EditComponent {
    detailView = false;
    searchView = false;
    searchSelect = 'Select Search Type';
    searchType: string;
    active = true;
    subResult: ReportMake;
    singleReport: any;
    returnData: Report[] = [];
    errorView = false;
    edit = false;
    returnUpdate: any;
    status = [
        {'id': 1, 'value': 'PENDING INVESTIGATION'},
        {'id': 2, 'value': 'CURRENTLY INVESTIGATING'},
        {'id': 3, 'value': 'CLOSED'},
    ]
    model = new MySearch(this.searchType, '',  this.status[0].id, '', 0);

    constructor(private reportservice: ReportService){}
    setType(searchType: string) {
        this.model.searchType =  searchType;
        this.searchSelect = searchType;
    }
    onSubmit() {
        this.searchView = true;
        this.detailView  = false;
        this.errorView = false;
        this.reportservice.adminSearch(this.model.searchType, this.model.searchParm, this.model.statusId)
        .then( result => {
            if (result.result === 'ERROR') {
                this.detailView  = false;
                this.searchView = false;
                this.errorView = true;
            } else {
                //this.submitted = true
                this.returnData = result.msg;
                //this.imageModel.id = result.msg.reference_no;
            }
        });
    }
    viewDetails(report: any) {
        this.detailView  = false;
        this.singleReport = {};
        this.singleReport = report;
        this.detailView  = true;
        this.searchView = false;
        this.model.id = this.singleReport.id
    }
    editMe(report: any) {
        this.edit = true;
        console.log(report);
    }
    updateStatus() {
        this.reportservice.updateStatus(this.model.statusId, this.model.id)
        .then( result => {
            if (result.result === 'ERROR') {
                this.errorView = true;
            } else {
                this.returnUpdate = result.msg;
            }
        });
    }
    addFeedback(){
        this.reportservice.addFeedBack(this.model.feedback, this.model.id)
        .then( result => {
            if (result.result === 'ERROR') {
               this.errorView = true;
            } else {
                this.returnUpdate = result.msg;
            }
        });
    }
}
