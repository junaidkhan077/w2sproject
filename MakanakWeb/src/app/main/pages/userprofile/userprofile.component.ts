import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Subject } from 'rxjs';
import { Router ,ActivatedRoute} from '@angular/router';
import {AppSettings} from '../../../app.setting'; 
import { HttpClient } from '@angular/common/http';

import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
    selector   : 'userprofile',
    templateUrl: './userprofile.component.html',
    styleUrls  : ['./userprofile.component.scss']
})
export class UserProfileComponent implements OnInit, OnDestroy
{
    form: FormGroup;
    param:any;
    is_update :any=false;
    userid :any=0;
    
    // Private
    private _unsubscribeAll: Subject<any>;

    /**
     * Constructor
     *
     * @param {FormBuilder} _formBuilder
     */
    constructor(
        private _formBuilder: FormBuilder,
        private router : Router,
        private http: HttpClient,
        public route : ActivatedRoute,
        private _snackBar: MatSnackBar
    )
    {
        // Set the private defaults
        this._unsubscribeAll = new Subject();
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Lifecycle hooks
    // -----------------------------------------------------------------------------------------------------

    /**
     * On init
     */
    ngOnInit(): void
    {
        // Reactive Form
        this.form = this._formBuilder.group({
            
            userName   : [
                {
                    value   : '',
                    disabled: true
                }, Validators.required
            ],

            firstName : ['', Validators.required],
            lastName  : ['', Validators.required],
            // userName  : [{disabled: true}, Validators.required],
            email     : ['', [Validators.required,Validators.email]],            
            phone   : ['', Validators.required],
            address1:[],
            address2:[],
            company:[],
            city:[],
            state:[],
            postalCode:[],
            country:[]
            
        });
        
        var userid=localStorage.getItem('userid')
        this.GetUserInfo(userid)
            
    }

    /**
     * On destroy
     */
    ngOnDestroy(): void
    {
        // Unsubscribe from all subscriptions
        this._unsubscribeAll.next();
        this._unsubscribeAll.complete();
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Finish the horizontal stepper
     */
    finishHorizontalStepper(): void
    {
        alert('You have finished the horizontal stepper!');
    }

    /**
     * Finish the vertical stepper
     */
    finishVerticalStepper(): void
    {
        alert('You have finished the vertical stepper!');
    }

    cancel_partner()
    {
        this.router.navigateByUrl("/pages/partners")
    }
   
    openSnackBar(message: string, action: string) {
        this._snackBar.open(message, action, {
          duration: 4000,
        });
      }

    GetUserInfo(userid){

        let token = localStorage.getItem('token');
        this.http.get(AppSettings.API_ENDPOINT + 'users/PartnersList/'+userid, 
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization':`Bearer ${token}`
                }
            },
        )    
          
          .subscribe((data: any) => {
    
            
            var result= data.Resp.data
            this.userid=result.user_id
            console.log(result)
            this.form.patchValue({
                firstName : result.first_name,
                lastName  : result.last_name,
                userName  : result.username,
                email     : result.primary_email,            
                phone     : result.primary_phone,
                address1  :result.address1,
                address2  :result.address2,
                company   :result.business_name,
                city      :result.city,
                state     :result.province,
                postalCode:result.postalcode,
                country   :result.country
              });
          
            },          
            error => {       
                this.openSnackBar('server error', 'failure')
            });
    }

    onSubmitPartner(){
        var formdata =this.form.getRawValue();
        let data =
        {
            'first_name':formdata.firstName,
            'last_name':formdata.lastName,
            'primary_email':formdata.email.trim(),
            'primary_phone':formdata.phone,
            'business_name':formdata.company,
            'address1':formdata.address1,
            'address2':formdata.address2,
            'city':formdata.city,
            'province':formdata.state,
            'country':formdata.country,
            'username':formdata.userName.trim(),
            'postalcode':formdata.postalCode,
            'is_approved':true,
            'is_lock':false,
            'allow_notifications':true,
            'user_id':this.userid,

        }

        // console.log( data, ' request ddata ' )
        
        if(!this.form.invalid)
        {


          let token = localStorage.getItem('token');

         
            this.http.post(AppSettings.API_ENDPOINT + 'users/UpdatePartners',data, 
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization':`Bearer ${token}`
                }
                
            },
             
        )    
          
          .subscribe((result: any) => {
              if(result.status='success'){
                  this.openSnackBar('user profile successfully', 'success')
                  this.router.navigateByUrl("/pages/partners")
              }
              else{
                this.openSnackBar('user profile failed', 'failue')
              }
                  
            },          
            error => {       
                this.openSnackBar('server error', 'failure')
            });

          

        }
       
    }


    
}
