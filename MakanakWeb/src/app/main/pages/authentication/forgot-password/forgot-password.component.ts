import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { FuseConfigService } from '@fuse/services/config.service';
import { fuseAnimations } from '@fuse/animations';
import { HttpClient } from '@angular/common/http';
import {Router,ActivatedRoute} from '@angular/router';
import {AppSettings} from '../../../../app.setting'; 
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
    selector     : 'forgot-password',
    templateUrl  : './forgot-password.component.html',
    styleUrls    : ['./forgot-password.component.scss'],
    encapsulation: ViewEncapsulation.None,
    animations   : fuseAnimations
})
export class ForgotPasswordComponent implements OnInit
{
    forgotPasswordForm: FormGroup;

    /**
     * Constructor
     *
     * @param {FuseConfigService} _fuseConfigService
     * @param {FormBuilder} _formBuilder
     */
    constructor(
        private _fuseConfigService: FuseConfigService,
        private _formBuilder: FormBuilder,
        public router: Router,private http: HttpClient,
        private _snackBar: MatSnackBar
    )
    {
        // Configure the layout
        this._fuseConfigService.config = {
            layout: {
                navbar   : {
                    hidden: true
                },
                toolbar  : {
                    hidden: true
                },
                footer   : {
                    hidden: true
                },
                sidepanel: {
                    hidden: true
                }
            }
        };
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Lifecycle hooks
    // -----------------------------------------------------------------------------------------------------

    /**
     * On init
     */
    ngOnInit(): void
    {
        this.forgotPasswordForm = this._formBuilder.group({
            email: ['', [Validators.required, Validators.email]]
        });
    }

    openSnackBar(message: string, action: string) {
        this._snackBar.open(message, action, {
          duration: 4000,
        });
      }


    onSubmitResetPwd(){

     
        let data = {
            "email": this.forgotPasswordForm.value.email
          } 
            this.http.post(AppSettings.API_ENDPOINT + 'users/resetpasswordtoken/',  data,
            {
              headers:{
                'Content-Type': 'application/json',
              }
            }
            )
            .subscribe((Resp: any) => {
                this.openSnackBar('email has been sent', 'success');
             
            },
            error => {       
                this.openSnackBar('email sent failed','failure');
            });
             

    }
}
