import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {PostMessage} from './message';

@Injectable()
export class HttpService{

    constructor(private http: HttpClient){ }

    postData(ms: PostMessage){
        const body = {message: ms.message};
        return this.http.post('http://localhost:4201/api/filter-bad-words/en-US', body);
    }
}
