import { Component } from '@angular/core';
import { MySearch } from '../model/mysearch';
import { Report } from '../model/report';
import { ReportService } from '../_service/report.service';

@Component({
    moduleId: module.id,
    selector: 'my-incident-form',
    templateUrl: `my-incident-form.component.html`
})
export class MyIncidentFormComponent {
    detailView = false;
    searchView = false;
    searchSelect = 'Select Search Type';
    searchType: string;
    active = true;
    singleReport: any;
    returnData: Report[] = [];
    model = new MySearch(this.searchType, '');
    errorView = false;
    constructor(private reportservice: ReportService){}

    setType(searchType: string) {
        this.model.searchType =  searchType;
        this.searchSelect = searchType;
    }
    onSubmit() {
        this.searchView = true;
        this.detailView  = false;
        this.errorView = false;
        this.reportservice.mySearch(this.model.searchType, this.model.searchParm)
        .then( result => {
            if (result.result === 'ERROR') {
                this.detailView  = false;
                this.searchView = false;
                this.errorView = true;
            }else {
                this.returnData = result.msg;
            }
        });
    }
    viewDetails(report: any) {
        this.detailView  = false;
        this.singleReport = {};
        this.singleReport = report;
        this.detailView  = true;
        this.searchView = false;
    }
    OpenImg(image: any) {
        var url = "http://lloyd-asus:8041/get_image?name="+ image.image_path;
        var win = window.open(url, '_blank');
        return false;
    }
}
