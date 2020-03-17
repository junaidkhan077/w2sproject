import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Subject } from 'rxjs';
import { Router ,ActivatedRoute} from '@angular/router';
import {AppSettings} from '../../../../app.setting'; 
import { HttpClient } from '@angular/common/http';

import {MatSnackBar} from '@angular/material/snack-bar';
// import { AESEncryptDecryptService } from '../../../../AESEncryptDecryptService';

// var CryptoJS = require('node-cryptojs-aes').CryptoJS;

@Component({
    selector   : 'managepartner',
    templateUrl: './managepartner.component.html',
    styleUrls  : ['./managepartner.component.scss']
})
export class ManagePartnerComponent implements OnInit, OnDestroy
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
        private _snackBar: MatSnackBar,
        // private _AESEncrypt: AESEncryptDecryptService
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

            this.route.queryParams
            .subscribe((v:any) => 
            {
                //  this.param=CryptoJS.AES.decrypt(v.param.trim(),'test').toString(CryptoJS.enc.Utf8); //this._AESEncrypt.decrypt(v.param.toString())               
                //  var decrypted = CryptoJS.AES.decrypt(v.param, 'test');
                //  this.param = decrypted.toString(CryptoJS.enc.Utf8);
                this.param=v.param
                if(this.param>0)
                {
                this.is_update=true;                
                this.GetPartnerInfo(this.param)
                }
            });

        // Reactive Form
        if(this.is_update){
        this.form = this._formBuilder.group({
            userName  : [{  value   : '',disabled: true}, Validators.required],
            firstName : ['', Validators.required],
            lastName  : ['', Validators.required],
            // userName  : ['', [Validators.required,Validators.email]],           
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
       }
       else{
            this.form = this._formBuilder.group({
                
                firstName : ['', Validators.required],
                lastName  : ['', Validators.required],
                // userName  : ['', [Validators.required,Validators.email]],
                userName  : ['', Validators.required],
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
            }
       
            
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

    GetPartnerInfo(userid){

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

        
        if(!this.form.invalid)
        {


          let token = localStorage.getItem('token');

          if(this.is_update){
          
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
                  this.openSnackBar('user updated successfully', 'success')
                  this.router.navigateByUrl("/pages/partners")
              }
              else{
                this.openSnackBar('user update failed', 'failue')
              }
                  
            },          
            error => {       
                this.openSnackBar('server error', 'failure')
            });

          }
          else{
          this.http.post(AppSettings.API_ENDPOINT + 'users/CreatePartners',data, 
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization':`Bearer ${token}`
                }
                
            },
             
        )    
          
          .subscribe((result: any) => {
            if(result.status='success'){
                this.openSnackBar('user created successfully', 'success')
                  this.SendResetPasswordLink(data.primary_email)
                  this.router.navigateByUrl("/pages/partners")
                }
                else{
                  this.openSnackBar('user create failed', 'failue')
                }
                  
            },          
            error => {       
                this.openSnackBar('server error', 'failure')
            });
        }

        }
       
    }


    SendResetPasswordLink(email){

     
        let data = {
            "email": email
          } 
            this.http.post(AppSettings.API_ENDPOINT + 'users/resetpasswordtoken/',  data,
            {
              headers:{
                'Content-Type': 'application/json',
              }
            }
            )
            .subscribe((Resp: any) => {
                this.openSnackBar('email sent successfully', 'success')
             
            },
            error => {       
                this.openSnackBar('email sent failed', 'failure')
            });
             

    }
}
