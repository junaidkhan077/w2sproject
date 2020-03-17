import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { FuseConfigService } from '@fuse/services/config.service';
import { fuseAnimations } from '@fuse/animations';
import { Router } from '@angular/router';
import { AuthenticationService } from '../login/authentication.service';
// import { ToastrService } from 'ngx-toastr';
import * as CryptoJS from 'crypto-js';
import { HttpClient } from '@angular/common/http';
import { first } from 'rxjs/operators';

import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
    selector     : 'login',
    templateUrl  : './login.component.html',
    styleUrls    : ['./login.component.scss'],
    encapsulation: ViewEncapsulation.None,
    animations   : fuseAnimations
})
export class LoginComponent implements OnInit
{
    loginForm: FormGroup;

    /**
     * Constructor
     *
     * @param {FuseConfigService} _fuseConfigService
     * @param {FormBuilder} _formBuilder
     */
    constructor(
        private _fuseConfigService: FuseConfigService,
        private _formBuilder: FormBuilder,
        private router:Router,

        // private toastrservice: ToastrService,
        public fb: FormBuilder, public authenticationService: AuthenticationService,      
        private http: HttpClient,
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
        this.loginForm = this._formBuilder.group({
            // email   : ['', [Validators.required, Validators.email]],
            email   : ['', Validators.required],
            password: ['', Validators.required]
        });
    }

    openSnackBar(message: string, action: string) {
        this._snackBar.open(message, action, {
          duration: 4000,
        });
      }


    onSubmitLogin(){
        // if(this.loginForm.value.email =='jax' && this.loginForm.value.password =='jax'){
        //     this.router.navigateByUrl("/apps/dashboards/analytics")
        // }

        var username = this.loginForm.value.email
        var password = this.loginForm.value.password
    
        console.log(username,password)
        this.authenticationService.login(username, password)
          .pipe(first())
          .subscribe(
            data => {
              setTimeout(() => {
                this.openSnackBar('Login success', 'success')
                this.router.navigateByUrl("/apps/dashboards/analytics")
              }, 3000);
            },
            error => {
                this.openSnackBar('Invalid username or password','failure')
                console.log(error)
            });
    }
}
