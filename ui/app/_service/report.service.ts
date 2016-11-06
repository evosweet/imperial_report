import { Injectable }     from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/toPromise';



@Injectable()
export class ReportService {

    public error: any;
    private report_url =  'http://lloyd-asus:8041'; // set url 
    //update_incident_status
    constructor (private http: Http) {}
    createUser(username: string, authType: number): Promise <any> {
        let headers = new Headers({'Content-Type': 'application/json', 'authToken': JSON.parse(localStorage.getItem('currentUser')).token});
        let body = JSON.stringify({'username': username, 'auth_id': authType})
        return this.http.post(this.report_url + '/create_user', body, {headers: headers})
         .toPromise()
         .then(this.extractData)
         .catch(this.handleError);

    }
    updateStatus(status_id: number|string, id: string| number): Promise <any> {
        let headers = new Headers({'Content-Type': 'application/json', 'authToken': JSON.parse(localStorage.getItem('currentUser')).token});
        let body = JSON.stringify({'status_id': status_id, 'id': id});
        return this.http.post(this.report_url + '/update_incident_status', body, {headers: headers})
         .toPromise()
         .then(this.extractData)
         .catch(this.handleError);
    }
    addFeedBack(feedback: string, incident_id: number): Promise <any> {
        let headers = new Headers({'Content-Type': 'application/json', 'authToken': JSON.parse(localStorage.getItem('currentUser')).token});
        let body = JSON.stringify({'comment': feedback, 'incident_id': incident_id});
        return this.http.post(this.report_url + '/add_feedback', body, {headers: headers})
         .toPromise()
         .then(this.extractData)
         .catch(this.handleError);
    }
    adminSearch(searchType: string, value: string, status: number): Promise <any> {
     let headers = new Headers({'Content-Type': 'application/json', 'authToken': JSON.parse(localStorage.getItem('currentUser')).token});
     let body = JSON.stringify({'searchType': searchType, 'value': value, 'status': status});
     return this.http.post(this.report_url + '/get_incident_2', body, {headers: headers})
     .toPromise()
     .then(this.extractData)
     .catch(this.handleError);
    }

    makeReport(event: number, location: string, description: string, district_id: number, phone?: string,
               email?: string, reportDate?: string): Promise <any> {
         let headers = new Headers({'Content-Type': 'application/json'});
         let body = JSON.stringify({'event_id': event, 'description': description , 'location': location,
                                    'contact_no': phone, 'email': email, 'dt_occured': reportDate, 'district_id': district_id
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
