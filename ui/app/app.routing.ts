import { NgModule } from '@angular/core';
import { Routes, RouterModule} from '@angular/router';
import { HomeComponent } from './component/home.component';
import { ReportComponent } from './component/report.component';
import { ViewRComponent } from './component/viewr.component';
import { ViewinstComponent } from './component/viewInst.component';
import { LoginComponent } from './component/login.component';
import { CreateComponent } from './component/admin/create.component';
import { AboutComponent } from './component/admin/about.component';
import { EditComponent } from './component/admin/edit.component';

import { AuthGuard } from './_guard/auth.guard';

const routers: Routes =  [
    {path: 'home', component: HomeComponent},
    {path: 'report', component: ReportComponent},
    {path: 'viewr', component: ViewRComponent},
    {path:'login', component: LoginComponent},
    {path: 'viewinst', component: ViewinstComponent, canActivate: [AuthGuard],
     children:[
         {path: '', component: AboutComponent},
         {path: 'create', component: CreateComponent},
         {path: 'edit', component: EditComponent }
     ]
    },
    {path: '', redirectTo: 'home', pathMatch: 'full'},
    {path: '**', component: HomeComponent }
];


@NgModule({
    imports: [RouterModule.forRoot(routers)],
    exports: [RouterModule]
})

export class AppRoutingModule {}

export const routingComponents = [ HomeComponent, ReportComponent, ViewRComponent, ViewinstComponent ]
;