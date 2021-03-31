import { Component} from '@angular/core';
import { HttpService} from './http.service';
import {PostMessage, InterfaceMessage} from './message';

@Component({
    selector: 'my-app',
    template: `<div class="form-group">
                    Message<Br>
                    <textarea class="comment" cols="30" rows="10" [(ngModel)]="ms.message"></textarea>
                </div>
                <div class="form-group">
                    <button class="btn btn-default" (click)="submit(ms)">Отправить</button>
                </div>
                <Br>
                <div *ngIf="done">
                    <div>Filtered message<Br>
                      <textarea class="comment" cols="30" rows="10">{{receivedUser.message}}</textarea>
                    </div>
                </div>`,
    providers: [HttpService]
})
export class AppComponent {

    ms: PostMessage=new PostMessage(); // данные вводимого пользователя

    receivedUser: InterfaceMessage; // полученный пользователь
    done: boolean = false;
    constructor(private httpService: HttpService){}
    submit(user: PostMessage){
        this.httpService.postData(user)
                .subscribe(
                    (data: InterfaceMessage) => {this.receivedUser=data; this.done=true;},
                    error => console.log(error)
                );
    }
}
