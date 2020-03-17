import {Component, OnInit, ViewChild} from '@angular/core';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import {AppSettings} from '../../../app.setting'; 
import { HttpClient } from '@angular/common/http';
import {Router,ActivatedRoute} from '@angular/router';
import { AuthenticationService } from '../authentication/login/authentication.service';
import {MatSnackBar} from '@angular/material/snack-bar';

// import { AESEncryptDecryptService } from '../../../AESEncryptDecryptService';
// var CryptoJS = require('node-cryptojs-aes').CryptoJS;


export interface UserData {
    sno: string;
    user_id: string;
    first_name: string;
    last_name : string;
    email : string;
    phone :string;
  }


  const users :any[] = []

  @Component({
    selector   : 'partner',
    templateUrl: './partner.component.html',
    styleUrls  : ['./partner.component.scss']
})


  export class PartnerComponent implements OnInit {
    displayedColumns: string[] = ['sno', 'first_name', 'last_name', 'email', 'phone','actions'];
    dataSource: MatTableDataSource<UserData>;
    
    @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
    @ViewChild(MatSort, {static: true}) sort: MatSort;

    constructor(public router: Router,private http: HttpClient,private authenticationService:AuthenticationService,
      private _snackBar: MatSnackBar,
      // private _AESEncrypt: AESEncryptDecryptService
      ) {
    //   const users = Array.from({length: 100}, (_, k) => createNewUser(k + 1));
  
      // Assign the data to the data source for the table to render
    //   this.dataSource = new MatTableDataSource(users);
    }
  
    ngOnInit() {
      this.PartnersList();
    //   this.dataSource.paginator = this.paginator;
    //   this.dataSource.sort = this.sort;
    }
  
    applyFilter(filterValue: string) {
      this.dataSource.filter = filterValue.trim().toLowerCase();
  
      if (this.dataSource.paginator) {
        this.dataSource.paginator.firstPage();
      }
    }
    
    openSnackBar(message: string, action: string) {
      this._snackBar.open(message, action, {
        duration: 4000,
      });
    }


    CreatePartner(){      
      //  var id = CryptoJS.AES.encrypt('0', 'test');
        //CryptoJS.AES.encrypt('0','test').toString();
      this.router.navigateByUrl('/pages/managepartner?param='+0);
    }
     
    EditUser(id: any)
    {
      // var userid = CryptoJS.AES.encrypt(id.toString(), 'test');// CryptoJS.AES.encrypt(id,'test').toString(); //this._AESEncrypt.encrypt(id.toString());
      this.router.navigateByUrl('/pages/managepartner?param='+id);
    }
    DeleteUser(id)
    {

     if(confirm("Are you sure you want to delete this user")) {      
        
      let token = localStorage.getItem('token');
        this.http.get(AppSettings.API_ENDPOINT + 'users/DeleteUser/'+id, 
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization':`Bearer ${token}`
                }
            },
        )    
          
          .subscribe((data: any) => {
             
            // if(data.status=='success'){
              this.openSnackBar('user deleted successfully', 'success')              
              this.PartnersList()
            // }
            // else{
            //   this.openSnackBar('user delete failed', 'failure') 
            // }
            },          
            error => {       
              this.openSnackBar('user delete failed', 'failure') 
            });
          }
    }
    PartnersList() {
        let token = localStorage.getItem('token');
        this.http.get(AppSettings.API_ENDPOINT + 'users/PartnersList/'+0, 
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization':`Bearer ${token}`
                }
            },
        )    
          
          .subscribe((result: any) => {
    
            users.length = 0;
            console.log(result, ' check data')
            if (result.Resp.data.length > 0) {    
                result.Resp.data.forEach(function (value, index) {
                let data: any;

                data = {
                  "sno": index + 1,
                  "user_id": value.user_id,
                  "first_name": value.first_name,
                  "last_name": value.last_name,
                  "email": value.primary_email,
                  "phone": value.primary_phone,
                },
                users.push(data)
              });
              this.dataSource = new MatTableDataSource(users);
              this.dataSource.paginator = this.paginator;
              this.dataSource.sort = this.sort;
            }
            },          
            error => {       
              this.openSnackBar('server error', 'failure') 
            });
      }

      

  }
  

  

