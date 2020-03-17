import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { AppSettings } from '../../../../app.setting';
import * as jwt_decode from 'jwt-decode';


import { Router, ActivatedRoute } from '@angular/router';
@Injectable({ providedIn: 'root' })
export class AuthenticationService {
    private currentUserSubject: BehaviorSubject<any>;
    public currentUser: Observable<any>;
    isRemberMeChecked: boolean = true;
    constructor(private http: HttpClient,private router:Router ) {
        // console.log(localStorage.getItem('currentUser'));
        this.currentUserSubject = new BehaviorSubject<any>(JSON.parse(localStorage.getItem('currentUser')));
        // console.log(this.currentUserSubject)
        this.currentUser = this.currentUserSubject.asObservable();
    }

    public get currentUserValue(): any {
        return JSON.parse(localStorage.getItem('currentUser'));
    }
    getToken(): string {
        return JSON.parse(localStorage.getItem('currentUser'))
    }

    login(username: string, password: string) {
        // console.log(username,password,'dddd')
        return this.http.post(AppSettings.API_ENDPOINT + 'token', { "username": username, "password": password },
            {
                headers: {
                    'Content-Type': 'application/json',
                }
            },
        )
            .pipe(map((user: any) => {
                var decoded = jwt_decode(user.access);
                

                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('userid', decoded.user_id);
                localStorage.setItem('decoded', decoded.exp);
                localStorage.setItem('token',user.access);
                localStorage.setItem('currentUserRefresh', JSON.stringify(user.refresh));
                localStorage.setItem('currentUsername', JSON.stringify(username));
                localStorage.setItem('Firsname', user.name);               
                localStorage.setItem('Role', user.role);              
                this.currentUserSubject.next(user);
                return user;
            }));
    }

    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('currentUser');
        localStorage.removeItem('currentUserRefresh');
        localStorage.removeItem('currentUsername');
        localStorage.removeItem('userid')
        localStorage.removeItem('Firsname');
        localStorage.removeItem('Role');
        localStorage.removeItem('token');
        localStorage.clear()
        this.currentUserSubject.next(null);
    }
}