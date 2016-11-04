import { NgModule } from '@angular/core';
import { Routes, RouterModule} from '@angular/router';
import { HomeComponent } from './component/home.component';
import { ReportComponent } from './component/report.component';
import { ViewRComponent } from './component/viewr.component';
import { ViewinstComponent } from './component/viewInst.component';

const routers: Routes =  [
    {path: 'home', component: HomeComponent},
    {path: 'report', component: ReportComponent},
    {path: 'viewr', component: ViewRComponent},
    {path: 'viewInst', component: ViewinstComponent},
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