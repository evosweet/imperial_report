import { Injectable }     from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/toPromise';



@Injectable()
export class ReportService {

    public error: any;
    private report_url =  'http://lloyd-asus:8041'; // set url 

    constructor (private http: Http) {}

    makeReport(event: number, location: string, description: string, phone?: string, 
               email?: string, reportDate?: string): Promise <any> {
         let headers = new Headers({'Content-Type': 'application/json'});
         let body = JSON.stringify({'event_id': event, 'description': description , 'location': location,
                                    'contact_no': phone, 'email': email, 'dt_occured': reportDate
                                });
         return this.http.post(this.report_url + '/make_report', body, {headers: headers})
         .toPromise()
         .then(this.extractData)
         .catch(this.handleError);
    }
    uploadImg(id: number, file: any): Promise <any> {
        let headers = new Headers({'Content-Type': 'image/png', 'INCIDENT-ID': id});
        return this.http.post(this.report_url + '/save_image', file, {headers: headers})
         .toPromise()
         .then(this.extractData)
         .catch(this.handleError);
    }
    mySearch(searchType: string, value: string | number) {
        console.log(searchType);
        console.log(value);
        let headers = new Headers({'Content-Type': 'application/json'});
        let body = JSON.stringify({'searchType': searchType, 'value': value});
        return this.http.post(this.report_url + '/get_incident', body, {headers: headers})
         .toPromise()
         .then(this.extractData)
         .catch(this.handleError);
    }
    extractData(res: Response) {
        let body = res.json();
        return body;
    }
    handleError(error: any) {
        return error.json();
    }
}

//get_incident