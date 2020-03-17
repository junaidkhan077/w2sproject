import { NgModule} from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { FuseSidebarModule } from '@fuse/components';

import { FuseSharedModule } from '@fuse/shared.module';
import { FuseDemoModule } from '@fuse/components/demo/demo.module';

import { LoginModule } from 'app/main/pages/authentication/login/login.module';
import { RegisterModule } from 'app/main/pages/authentication/register/register.module';
import { ForgotPasswordModule } from 'app/main/pages/authentication/forgot-password/forgot-password.module';
import { ResetPasswordModule } from 'app/main/pages/authentication/reset-password/reset-password.module';
import { LockModule } from 'app/main/pages/authentication/lock/lock.module';
import { MailConfirmModule } from 'app/main/pages/authentication/mail-confirm/mail-confirm.module';
import { ComingSoonModule } from 'app/main/pages/coming-soon/coming-soon.module';
import { Error404Module } from 'app/main/pages/errors/404/error-404.module';
import { Error500Module } from 'app/main/pages/errors/500/error-500.module';
import { InvoiceModernModule } from 'app/main/pages/invoices/modern/modern.module';
import { InvoiceCompactModule } from 'app/main/pages/invoices/compact/compact.module';
import { MaintenanceModule } from 'app/main/pages/maintenance/maintenence.module';
import { PricingModule } from 'app/main/pages/pricing/pricing.module';
import { ProfileModule } from 'app/main/pages/profile/profile.module';
import { SearchClassicModule } from 'app/main/pages/search/classic/search-classic.module';
import { SearchModernModule } from 'app/main/pages/search/modern/search-modern.module';
import { FaqModule } from 'app/main/pages/faq/faq.module';
import { KnowledgeBaseModule } from 'app/main/pages/knowledge-base/knowledge-base.module';

import { PartnerComponent } from 'app/main/pages/partner/partner.component';
import { RouterModule, Routes } from '@angular/router';
import {ManagePartnerComponent} from 'app/main/pages/partner/managepartner/managepartner.component';
import {MatSnackBar, MatSnackBarModule} from '@angular/material/snack-bar';

import { MatFormFieldModule, MatInputModule, MatPaginatorModule, MatTableModule, MatSortModule } from '@angular/material';

import { MatSelectModule } from '@angular/material/select';
import { MatStepperModule } from '@angular/material/stepper';
import { FormsComponent } from 'app/main/ui/forms/forms.component';

import { UserProfileComponent } from 'app/main/pages/userprofile/userprofile.component';
import { DashboardComponent } from 'app/main/pages/dashboard/dashboard.component';


const routes: Routes = [
    // Carded
    {
        path     : 'partners',
        component: PartnerComponent
    },
    {
        path :'managepartner',
       component : ManagePartnerComponent
    },
    {
        path : 'userprofile',
        component : UserProfileComponent
    },
    {
        path     : 'dash',
        component: DashboardComponent
    },
   
]

@NgModule({
    declarations: [
        PartnerComponent,
        ManagePartnerComponent,
        UserProfileComponent,
        FormsComponent,
        DashboardComponent,
    ],
    imports: [
        // Authentication
        RouterModule.forChild(routes),
       
        LoginModule,
        RegisterModule,
        ForgotPasswordModule,
        ResetPasswordModule,
        LockModule,
        MailConfirmModule,

        // Coming-soon
        ComingSoonModule,

        // Errors
        Error404Module,
        Error500Module,

        // Invoices
        InvoiceModernModule,
        InvoiceCompactModule,

        // Maintenance
        MaintenanceModule,

        // Pricing
        PricingModule,

        // Profile
        ProfileModule,

        // Search
        SearchClassicModule,
        SearchModernModule,

        // Faq
        FaqModule,

        // Knowledge base
        KnowledgeBaseModule,

        //partner

        MatButtonModule,
        MatIconModule,
        MatTabsModule,
        FuseSidebarModule,
        FuseSharedModule,
        FuseDemoModule,
        MatFormFieldModule, 
        MatInputModule, 
        MatPaginatorModule, 
        MatTableModule, 
        MatSortModule, 
        MatSelectModule,
        MatStepperModule,
        MatSnackBarModule,        
    ]
})
export class PagesModule
{

}
